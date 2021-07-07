from allauth.account.adapter import DefaultAccountAdapter
from django.core.exceptions import ValidationError


class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/home"
        return path.format(username=request.user.username)

    def clean_email(self,email):
        RestrictedList = ['Your restricted list goes here.']
        if email in RestrictedList:
            raise ValidationError('You are restricted from registering. Please contact admin.')
        return email


