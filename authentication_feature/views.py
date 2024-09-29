from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import AccountTypeForm, TenantRegistrationForm, LandlordRegistrationForm, CustomUserChangeForm
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
    if account_type.casefold() == AccountType.TENANT.casefold():
        form_class = TenantRegistrationForm
    elif account_type.casefold() == AccountType.LANDLORD.casefold():
        form_class = LandlordRegistrationForm
    else:
        return redirect('account_type_selection')

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = form_class()
    
    return render(request, 'register.html', {'form': form, 'account_type': account_type})

@login_required
def update_user_info(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to a profile page or any other page
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'update_user_info.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def custom_logout(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, 'home.html')