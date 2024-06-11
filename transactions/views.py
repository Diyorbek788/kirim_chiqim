from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, TransactionForm
from .models import Transaction
from django.urls import reverse

def register(request):
    """
    Handle the user registration process.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the registration form.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """
    Handle the user login process.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the login form or a redirect to the dashboard on successful login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_authenticated:
            login(request, user)
            return redirect(reverse('dashboard'))
        else:
            return render(request, 'login.html', {'error': 'Incorrect username or password'})
    else:
        return render(request, 'login.html')

def logout_view(request):
    """
    Handle the user logout process.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: A redirect to the login page.
    """
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    """
    Display the user's dashboard with their income and expense transactions.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the dashboard template.
    """
    incomes = Transaction.objects.filter(user=request.user, transaction_type='income')
    expenses = Transaction.objects.filter(user=request.user, transaction_type='expense')
    return render(request, 'dashboard.html', {'incomes': incomes, 'expenses': expenses})

@login_required
def add_transaction(request):
    """
    Handle the process of adding a new transaction.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object with the add transaction form or a redirect to the dashboard on successful submission.
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            if request.user.is_authenticated:
                transaction.user = request.user
            transaction.transaction_type = request.path_info.split('/')[2]  # Extracts the type from the URL
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

@login_required
def edit_transaction(request, id):
    """
    Handle the process of editing an existing transaction.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the transaction to edit.

    Returns:
        HttpResponse: The response object with the edit transaction form or a redirect to the dashboard on successful submission.
    """
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'edit_transaction.html', {'form': form})

@login_required
def delete_transaction(request, id):
    """
    Handle the process of deleting an existing transaction.

    Args:
        request (HttpRequest): The request object.
        id (int): The ID of the transaction to delete.

    Returns:
        HttpResponse: The response object with the delete confirmation or a redirect to the dashboard on successful deletion.
    """
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('dashboard')
    return render(request, 'delete_transaction.html', {'transaction': transaction})
