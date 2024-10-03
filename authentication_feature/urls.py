from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from utilities.decorators import anonymous_required
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'), 
    
    # Account type selection
    path('select-account-type/', anonymous_required(views.account_type_selection), name='account_type_selection'),
    
    # Registration
    path('register/<str:account_type>/', anonymous_required(views.register), name='register'),
    
    # Update user info
    path('update-user-info/', login_required(views.update_user_info), name='update_user_info'),
    
    # User profile
    path('profile/', login_required(views.profile), name='profile'),
    
    # Login
    path('login/', anonymous_required(LoginView.as_view(template_name='login.html', next_page='home')), name='login'),
    
    # Logout
    path('logout/', login_required(LogoutView.as_view(template_name=None, next_page='home'), redirect_field_name=None), name='logout'),
    
    # Change password
    path('change-password/', login_required(views.change_password), name='change_password'),
]