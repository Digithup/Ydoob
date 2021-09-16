from .models import Notification

def create_notification_admin(request, to_user, notification_type, extra_id=0 ,extra_info=0):

    for user in to_user:
     notification = Notification.objects.create(to_user=user, notification_type=notification_type, created_by=request.user, extra_id=extra_id,
                                               extra_info=extra_info)

def create_notification_vendor(request, to_user, notification_type, extra_id=0, extra_info=0):


 notification = Notification.objects.create(to_user=to_user, notification_type=notification_type,
                                            created_by=request.user, extra_id=extra_id,
                                            extra_info=extra_info)