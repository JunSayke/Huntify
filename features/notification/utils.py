def create_notification(user, title, message):
    from .models import Notification
    Notification.objects.create(user=user, title=title, message=message)
