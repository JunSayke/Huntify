# urls.py
from django.urls import path
from . import views

app_name = 'address'

# TODO: Secure Endpoints
urlpatterns = [
    path('ajax/provinces/', views.get_provinces, name='get-provinces'),
    path('ajax/provinces/<int:province_id>/municipalities/', views.get_province_municipalities,
         name='get-province-municipalities'),
    path('ajax/municipalities/<int:municipality_id>/barangays/', views.get_municipality_barangays,
         name='get-municipality-barangays'),
]
