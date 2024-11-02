from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import LoginView
from .forms import AccountTypeForm, RegistrationForm, CustomUserChangeForm, CustomAuthenticationForm
from .models import AccountType
from django.contrib.auth.models import Group

from django.http import HttpResponseForbidden

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
        # This will validate and raise ValueError if the account type is invalid
        account_type = AccountType(account_type).value
    except ValueError:
        return redirect('account_type_selection')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.account_type = account_type
            user = form.save()

            # Assign user to group based on account type using the AccountType enum
            group = None
            if account_type == AccountType.LANDLORD:
                group = Group.objects.get(name='landlord')
            elif account_type == AccountType.TENANT:
                group = Group.objects.get(name='tenant')

            if group:
                user.groups.add(group)
                
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


def profile(request):
    if request.user.account_type == AccountType.TENANT:
        return render(request, 'profile.html')
    else:
        return HttpResponseForbidden("You are not allowed to access this page.")

def landlord_account(request):
    if request.user.account_type == AccountType.LANDLORD:
        return render(request, 'landlord_account.html')
    else:
        return HttpResponseForbidden("You are not allowed to access this page.")
