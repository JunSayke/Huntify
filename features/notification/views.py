from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Notification

# Create your views here.


@login_required
def notification_list(request):
    notifications = request.user.notifications.all()
    
    # Render notifications in HTML format
    return render(request, 'notification/notifications.html', {'notifications': notifications})


@csrf_exempt  # Required for POST requests without a CSRF token (if applicable)
@login_required
def mark_as_read(request, pk):
    if request.method == "POST":
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'message': 'Notification marked as read'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
@login_required
def delete_notification(request, pk):
    if request.method == "DELETE":
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.delete()
        return JsonResponse({'message': 'Notification deleted'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

