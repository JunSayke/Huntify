from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this line for the home view
    path('select-account-type/', views.account_type_selection, name='account_type_selection'),
    path('register/<str:account_type>/', views.register, name='register'),
    path('update-user-info/', views.update_user_info, name='update_user_info'),
    path('profile/', views.profile, name='profile'),
    path('login/', LoginView.as_view(template_name='login.html', next_page='profile'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
]