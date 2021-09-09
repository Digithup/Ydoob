from django.urls import path, include

from .views import notifications


app_name = 'notifications'
urlpatterns = [
    path('notifications/', notifications, name='notifications'),
]