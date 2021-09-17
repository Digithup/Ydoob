from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError
User = get_user_model()
class DeliverySignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=250)
  first_name = forms.CharField(max_length=150)
  last_name = forms.CharField(max_length=150)

  class Meta:
    model = User
    fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

  def clean_email(self):
    email = self.cleaned_data['email'].lower()
    if User.objects.filter(email=email):
      raise ValidationError("This email address already exists.")
    return email

class DeliveryLoginForm(forms.Form):
  """
  Description:A form that will be used by user's to login.\n
  """
  email = forms.EmailField(label='Email')
  password = forms.CharField(widget=forms.PasswordInput)

  def clean(self, *args, **kwargs):
    email = self.cleaned_data.get("email")
    password = self.cleaned_data.get("password")

    if email and password:
      user = authenticate(email=email, password=password)

      if not user:
        raise forms.ValidationError("Incorrect Information  . Please Login Again")

      if not user.check_password(password):
        raise forms.ValidationError("Incorrect Password")

      if not user.active:
        raise forms.ValidationError("This user is not longer active.")

    return super(DeliveryLoginForm, self).clean(*args, **kwargs)


