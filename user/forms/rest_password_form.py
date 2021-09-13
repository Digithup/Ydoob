# import unicodedata
#
#
# from django import forms
# from django.contrib.auth import (
#     authenticate, get_user_model, password_validation,
# )
# from django.contrib.auth.hashers import (
#     UNUSABLE_PASSWORD_PREFIX, identify_hasher,
# )
# from django.contrib.auth.models import User
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.exceptions import ValidationError
# from django.core.mail import EmailMultiAlternatives
# from django.template import loader
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode
# from django.utils.text import capfirst
#
# from DNigne.settings import gettext
#
# UserModel = get_user_model()
#
#
# def _unicode_ci_compare(s1, s2):
#     """
#     Perform case-insensitive comparison of two identifiers, using the
#     recommended algorithm from Unicode Technical Report 36, section
#     2.11.2(B)(2).
#     """
#     return unicodedata.normalize('NFKC', s1).casefold() == unicodedata.normalize('NFKC', s2).casefold()
#
#
# class ReadOnlyPasswordHashWidget(forms.Widget):
#     template_name = 'auth/widgets/read_only_password_hash.html'
#     read_only = True
#
#     def get_context(self, name, value, attrs):
#         context = super().get_context(name, value, attrs)
#         summary = []
#         if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
#             summary.append({'label': gettext("No password set.")})
#         else:
#             try:
#                 hasher = identify_hasher(value)
#             except ValueError:
#                 summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
#             else:
#                 for key, value_ in hasher.safe_summary(value).items():
#                     summary.append({'label': gettext(key), 'value': value_})
#         context['summary'] = summary
#         return context
#
#
# class ReadOnlyPasswordHashField(forms.Field):
#     widget = ReadOnlyPasswordHashWidget
#
#     def __init__(self, *args, **kwargs):
#         kwargs.setdefault("required", False)
#         kwargs.setdefault('disabled', True)
#         super().__init__(*args, **kwargs)
#
#
# class UsernameField(forms.CharField):
#     def to_python(self, value):
#         return unicodedata.normalize('NFKC', super().to_python(value))
#
#     def widget_attrs(self, widget):
#         return {
#             **super().widget_attrs(widget),
#             'autocapitalize': 'none',
#             'autocomplete': 'username',
#         }
#
#
# class UserCreationForm(forms.ModelForm):
#     """
#     A form that creates a user, with no privileges, from the given username and
#     password.
#     """
#     error_messages = {
#         'password_mismatch': _('The two password fields didn’t match.'),
#     }
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )
#
#     class Meta:
#         model = User
#         fields = ("username",)
#         field_classes = {'username': UsernameField}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self._meta.model.USERNAME_FIELD in self.fields:
#             self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         return password2
#
#     def _post_clean(self):
#         super()._post_clean()
#         # Validate the password after self.instance is updated with form data
#         # by super().
#         password = self.cleaned_data.get('password2')
#         if password:
#             try:
#                 password_validation.validate_password(password, self.instance)
#             except ValidationError as error:
#                 self.add_error('password2', error)
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField(
#         label=_("Password"),
#         help_text=_(
#             'Raw passwords are not stored, so there is no way to see this '
#             'user’s password, but you can change the password using '
#             '<a href="{}">this form</a>.'
#         ),
#     )
#
#     class Meta:
#         model = User
#         fields = '__all__'
#         field_classes = {'username': UsernameField}
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         password = self.fields.get('password')
#         if password:
#             password.help_text = password.help_text.format('../password/')
#         user_permissions = self.fields.get('user_permissions')
#         if user_permissions:
#             user_permissions.queryset = user_permissions.queryset.select_related('content_type')
#
#
# class AuthenticationForm(forms.Form):
#     """
#     Base class for authenticating users. Extend this to get a form that accepts
#     username/password logins.
#     """
#     username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
#     password = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
#     )
#
#     error_messages = {
#         'invalid_login': _(
#             "Please enter a correct %(username)s and password. Note that both "
#             "fields may be case-sensitive."
#         ),
#         'inactive': _("This account is inactive."),
#     }
#
#     def __init__(self, request=None, *args, **kwargs):
#         """
#         The 'request' parameter is set for custom auth use by subclasses.
#         The form data comes in via the standard 'data' kwarg.
#         """
#         self.request = request
#         self.user_cache = None
#         super().__init__(*args, **kwargs)
#
#         # Set the max length and label for the "username" field.
#         self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
#         username_max_length = self.username_field.max_length or 254
#         self.fields['username'].max_length = username_max_length
#         self.fields['username'].widget.attrs['maxlength'] = username_max_length
#         if self.fields['username'].label is None:
#             self.fields['username'].label = capfirst(self.username_field.verbose_name)
#
#     def clean(self):
#         username = self.cleaned_data.get('username')
#         password = self.cleaned_data.get('password')
#
#         if username is not None and password:
#             self.user_cache = authenticate(self.request, username=username, password=password)
#             if self.user_cache is None:
#                 raise self.get_invalid_login_error()
#             else:
#                 self.confirm_login_allowed(self.user_cache)
#
#         return self.cleaned_data
#
#     def confirm_login_allowed(self, user):
#         """
#         Controls whether the given User may log in. This is a policy setting,
#         independent of end-user authentication. This default behavior is to
#         allow login by active users, and reject login by inactive users.
#
#         If the given user cannot log in, this method should raise a
#         ``ValidationError``.
#
#         If the given user may log in, this method should return None.
#         """
#         if not user.is_active:
#             raise ValidationError(
#                 self.error_messages['inactive'],
#                 code='inactive',
#             )
#
#     def get_user(self):
#         return self.user_cache
#
#     def get_invalid_login_error(self):
#         return ValidationError(
#             self.error_messages['invalid_login'],
#             code='invalid_login',
#             params={'username': self.username_field.verbose_name},
#         )
#
#
#
#
#
#
#
#
# class PasswordChangeForm(SetPasswordForm):
#     """
#     A form that lets a user change their password by entering their old
#     password.
#     """
#     error_messages = {
#         **SetPasswordForm.error_messages,
#         'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
#     }
#     old_password = forms.CharField(
#         label=_("Old password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True}),
#     )
#
#     field_order = ['old_password', 'new_password1', 'new_password2']
#
#     def clean_old_password(self):
#         """
#         Validate that the old_password field is correct.
#         """
#         old_password = self.cleaned_data["old_password"]
#         if not self.user.check_password(old_password):
#             raise ValidationError(
#                 self.error_messages['password_incorrect'],
#                 code='password_incorrect',
#             )
#         return old_password
#
#
# class AdminPasswordChangeForm(forms.Form):
#     """
#     A form used to change the password of a user in the admin interface.
#     """
#     error_messages = {
#         'password_mismatch': _('The two password fields didn’t match.'),
#     }
#     required_css_class = 'required'
#     password1 = forms.CharField(
#         label=_("Password"),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'autofocus': True}),
#         strip=False,
#         help_text=password_validation.password_validators_help_text_html(),
#     )
#     password2 = forms.CharField(
#         label=_("Password (again)"),
#         widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
#         strip=False,
#         help_text=_("Enter the same password as before, for verification."),
#     )
#
#     def __init__(self, user, *args, **kwargs):
#         self.user = user
#         super().__init__(*args, **kwargs)
#
#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')
#         if password1 and password2 and password1 != password2:
#             raise ValidationError(
#                 self.error_messages['password_mismatch'],
#                 code='password_mismatch',
#             )
#         password_validation.validate_password(password2, self.user)
#         return password2
#
#     def save(self, commit=True):
#         """Save the new password."""
#         password = self.cleaned_data["password1"]
#         self.user.set_password(password)
#         if commit:
#             self.user.save()
#         return self.user
#
#     @property
#     def changed_data(self):
#         data = super().changed_data
#         for name in self.fields:
#             if name not in data:
#                 return []
#         return ['password']
