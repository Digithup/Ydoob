from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.decorators import login_required
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

from sales.models.orders import OrderProduct, Order
from user.decorators import unauthenticated_user, allowed_users
from user.forms.forms import UserSignUpForm, UserLoginForm, UserUpdateImageForm, UserUpdateProfileForm, \
    UserUpdateAddressForm
from user.forms.forms import PasswordResetForm, SetPasswordForm
from user.models import UserAddress
from user.signals import user_logged_in


class DeliveryLoginView(View):
    """
    Description:Will be used to login and logout Users.\n
    """
    template_name = 'DeliveryAdmin/Delivery_login.html'

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('DeliverySystem:DeliveryIndex')
        else:
            form = UserLoginForm()
            context = {
                "title": "Login",
                "form": form
            }
            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserLoginForm(request.POST or None)

        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                user_logged_in.send(
                    user.__class__,
                    instance=user,
                    request=request
                )
                try:
                    del request.session['guest_email_id']

                except:
                    pass

                if is_safe_url(redirect_path, request.get_host()):
                    return redirect(redirect_path)

                else:
                    return redirect("/")

            else:
                print("error")
                return redirect("/delivery/login/")

        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)


def DeliveryDashboard(request):
    return render(request, 'DeliveryAdmin/delivery-base/index.html')


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