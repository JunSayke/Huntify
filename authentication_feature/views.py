from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from .forms import AccountTypeForm, RegistrationForm, CustomUserChangeForm, CustomAuthenticationForm
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
        print(account_type)
        account_type = AccountType(account_type).value
        print(account_type)
    except ValueError:
        return redirect('account_type_selection')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.account_type = account_type
            user = form.save()
            print(user.account_type)
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

class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = CustomAuthenticationForm
    next_page = "home"