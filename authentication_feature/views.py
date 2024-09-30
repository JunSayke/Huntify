from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import AccountTypeForm, RegistrationForm, CustomUserChangeForm
from .models import AccountType

def account_type_selection(request):
    if request.method == 'POST':
        form = AccountTypeForm(request.POST)
        if form.is_valid():
            account_type = form.cleaned_data['account_type']
            return redirect('register', account_type=account_type)
    else:
        form = AccountTypeForm()
    return render(request, 'account_type_selection.html', {'form': form})

def register(request, account_type):
    try:
        # Raises ValueError if the account type is invalid
        account_type = AccountType(account_type).label
    except ValueError:
        return redirect('account_type_selection')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.account_type = account_type
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form, 'account_type': account_type})

def update_user_info(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'update_user_info.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def home(request):
    return render(request, 'home.html')

