from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notification_list, name='notification_list'),
    path('notification/<int:pk>/mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('notification/<int:pk>/delete/', views.delete_notification, name='delete_notification'),
]

