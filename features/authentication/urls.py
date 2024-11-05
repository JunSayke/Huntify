from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from utilities.decorators import anonymous_required

app_name = "authentication"
urlpatterns = [
    path("register/", anonymous_required(views.RegistrationWizard.as_view()), name="register"),
    path("login/", anonymous_required(views.LoginView.as_view()), name="login"),
    path("logout/", login_required(views.LogoutView.as_view()), name="logout"),
    path("home/", views.home, name="home"),
    path("profile/<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("profile/<str:username>/", views.ProfileView.as_view(), name="profile-by-username"),
    path("profile/", views.ProfileView.as_view(), name="my-profile"),
    path("change-password/", login_required(views.change_password), name="change-password"),
    path("profile/edit", login_required(views.UpdateProfileView.as_view()), name="edit-profile"),
    path("additional-info/", login_required(views.AdditionalInfoView.as_view()), name="personal-information"),
]
