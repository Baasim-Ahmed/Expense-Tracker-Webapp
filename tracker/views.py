from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .forms import TransactionForm
from django.shortcuts import get_object_or_404
import calendar
from django.db.models.functions import ExtractMonth
from django.contrib.auth.models import User

@login_required
def dashboard_view(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-timestamp')

    # Filters from query parameters
    selected_month = request.GET.get('month')
    selected_category = request.GET.get('category')

    if selected_month:
        transactions = transactions.filter(timestamp__month=selected_month)

    if selected_category:
        transactions = transactions.filter(category=selected_category)

    income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    balance = income - expenses

    # For filters dropdowns
    months = list(range(1, 13))
    categories = Transaction.objects.filter(user=request.user).values_list('category', flat=True).distinct()

    return render(request, "tracker/dashboard.html", {
        "transactions": transactions,
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "months": [(i, calendar.month_name[i]) for i in months],
        "selected_month": int(selected_month) if selected_month else None,
        "selected_category": selected_category,
        "categories": categories,
    })

def register_view(request):
   if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'register.html', {'error': "Passwords do not match"})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': "Username already taken"})

        # ✅ Safe to create and log in the user now
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('dashboard')  # or wherever your main page is
   return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def add_transaction_view(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            txn = form.save(commit=False)
            txn.user = request.user
            txn.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})

def edit_transaction_view(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=txn)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=txn)
    return render(request, 'tracker/edit_transaction.html', {'form': form, 'txn': txn})

@login_required
def delete_transaction_view(request, pk):
    txn = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == 'POST':
        txn.delete()
        return redirect('dashboard')
    return render(request, 'tracker/delete_transaction.html', {'txn': txn})