from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import resolve_url, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode, is_safe_url
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from social_django.models import UserSocialAuth

from DeliverySystem.forms import DeliveryLoginForm, DeliverySignUpForm
from sales.models.orders import OrderProduct, Order
from user.decorators import unauthenticated_user, allowed_users
from user.forms.forms import UserSignUpForm, UserLoginForm, UserUpdateImageForm, UserUpdateProfileForm, \
    UserUpdateAddressForm
from user.forms.forms import PasswordResetForm, SetPasswordForm
from user.models import UserAddress
from user.signals import user_logged_in


@unauthenticated_user
def DeliverySignup(request):
    if request.method == 'GET':
        signup_form = DeliverySignUpForm()
        return render(request, 'DeliveryAdmin/Delivery_login.html', {'signup_form': signup_form})
    if request.method == 'POST':
        signup_form = DeliverySignUpForm(request.POST)
        # print(form.errors.as_data())
        if signup_form.is_valid():
            groups = Group.objects.get_or_create(name='delivery')

            user = signup_form.save(commit=False)
            user.is_active = False
            #user.groups.set='delivery'

            user.save()
            user.groups.set('delivery')
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('register/deliveryActiveEmailMessage.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'register/deliveryActiveEmailSent.html')
        else:
            messages.error(request, "Error")
            print(request.POST)
    else:

        form = DeliverySignUpForm()
    return render(request, 'DeliveryAdmin/Delivery_login.html', {'signup_form': signup_form})

class DeliveryLoginView(View):
    """
    Description:Will be used to login and logout users.\n
    """
    template_name = 'DeliveryAdmin/Delivery_login.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('DeliverySystem:DeliveryIndex')
        else:
            login_form = UserLoginForm()
            signup_form = DeliverySignUpForm()
            context = {
                "title": "Login",
                "login_form": login_form,
                "signup_form": signup_form,
            }
            return render(request, self.template_name, context)
    def post(self, request, *args, **kwargs):
        login_form = UserLoginForm(request.POST or None)

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if login_form.is_valid():
            email = login_form.cleaned_data.get("email")
            password = login_form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                user_logged_in.send(
                    user.__class__,
                    instance=user,
                    request=request
                )
                if is_safe_url(redirect_path, request.get_host()):
                    return HttpResponseRedirect(reverse_lazy('DeliverySystem:DeliveryIndex'))
                    print('super')

                else:
                    messages.error(request, "Error")
                    print(request.POST)
                    print(request)
                    return HttpResponseRedirect(reverse_lazy('DeliverySystem:DeliveryIndex'))

            else:
                print("error")
                messages.error(request, "Error")
                return HttpResponseRedirect(reverse_lazy('DeliverySystem:DeliveryLogin'))

        context = {
            "title": "Login",
            "login_form": login_form
        }
        return render(request, self.template_name, context)


def DeliveryLogout(request):
    logout(request)
    return redirect('DeliverySystem:DeliveryLogin')


@login_required(login_url='/delivery/login')  # Check login
#@allowed_users(allowed_roles=['admin'])
def DeliveryDashboard(request):
    if request.user.is_authenticated:
        return render(request, 'DeliveryAdmin/delivery-base/index.html')
    else:
        form = DeliveryLoginForm()

        context = {
            "title": "Login",
            "form": form
        }
        return HttpResponseRedirect(reverse_lazy('DeliveryLoginView'))



def DeliveryOrder(request):
    orders=Order.objects.filter(orderproduct__delivery_by='Ydoob')

    context={
        'orders':orders
    }
    return render(request, 'DeliveryOrder/DeliveryOrder.html',context)


# class OrdersListView(ListView):
#     model = Order
#     template_name = 'sales/orders/admin-orders.html'
#     paginate_by = 5  # if pagination is desired
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['now'] = timezone.now()
#         return context
#
#     @method_decorator(allowed_users(allowed_roles=['admin']))
#     def dispatch(self, *args, **kwargs):
#         return super(OrdersListView, self).dispatch(*args, **kwargs)