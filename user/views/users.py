import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import is_safe_url, urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView

from core.decorators import anonymous_required
from user.decorators import unauthenticated_user
from user.signals import user_logged_in
from user.forms.forms import UserLoginForm, CustomerRegisterForm
from user.utils import account_activation_token

User = get_user_model()
@login_required(login_url='/login') # Check login
def profile(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = User.objects.get(user_id=current_user.id)
    context = {'current_user': current_user,
               'profile':profile}
    return render(request, 'users/customers/CustomerProfile.html', context)



class CustomerLogin(View):
    """
    Description:Will be used to login and logout users.\n
    """
    template_name = 'users/customers/CustomerLogin.html'

    def get(self, request, *args, **kwargs):
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
                return redirect("/home/login/")

        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)

class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})


class RegistrationView(View):
    def get(self, request):
        return render(request, 'users/customers/CustomerRegister.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user users


        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(email=email).exists():
            if len(password) < 6:
                messages.error(request, 'Password too short')
                return render(request, 'users/customers/CustomerRegister.html', context)

            user = User.objects.create_user( email=email)
            user.set_password(password)
            user.active = False
            user.is_seller = False
            user.save()
            current_site = get_current_site(request)
            email_body = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }

            link = reverse('activate', kwargs={
                'uidb64': email_body['uid'], 'token': email_body['token']})

            email_subject = 'Activate your users'

            activate_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                'Hi ' + user.username + ', Please the link below to activate your users \n' + activate_url,
                'noreply@semycolon.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'Account successfully created')
            return render(request, 'users/customers/CustomerRegister.html')

class Verification(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.active and user.is_seller:
                return redirect('login')
            user.active = True
            user.is_seller = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class CustomerRegister(CreateView):
    model = User
    form_class = CustomerRegisterForm
    template_name = 'users/customers/CustomerRegister.html'

    # uccess_url =redirect('home:Products_admin')
    success_url = reverse_lazy('home:index')

def customer_logout(request):
    logout(request)
    return redirect('home:index')

