from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from user.admin import UserAdmin
from user.forms import GuestForm, UserAdminChangeForm
from django.utils.http import is_safe_url
from user.signals import user_logged_in
from django.views.generic import CreateView, TemplateView, UpdateView
from django.views import View, generic

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

from user.models import GuestEmail, User
from user.forms import UserLoginForm, UserRegisterForm




def user_profile(request, id):
    user = User.objects.get(id=id)

    context = {'user': user,
              }
    return render(request, 'accounts/user_profile.html', context)


def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_delete = True
    user.save()
    return redirect('users:user_list')


def update_profile(request):
    user = User.objects.get(id=request.user.id)
    forms = UserAdminChangeForm(instance=user)
    if request.method == 'POST':
        forms = UserAdminChangeForm(request.POST, request.FILES, instance=user)
        if forms.is_valid():
            forms.save()
    context = {
        'user': user,
        'forms': forms
    }
    return render(request, 'accounts/test.html', context)


class AddProfile(CreateView):
    model = User
    template_name = 'accounts/UpdateProfile.html'
    fields = '__all__'
    # uccess_url =redirect('home:Products_admin')
    success_url = reverse_lazy('users:user_profile')


class EditProfile(UpdateView):
    model = User
    fields = '__all__'
    template_name = 'accounts/UpdateProfile.html'
    success_url = reverse_lazy('users:user_profile')






# class RegisterView(CreateView):
#     form_class = UserRegisterForm
#     template_name = 'users/create_storetrach.html'
#     success_url = '/login/'


class RegisterView(View):
    """
    Description:View to create a new user.\n
    """
    template_name = 'users/create-user.html'

    def get(self, request, *args, **kwargs):
        form = UserRegisterForm()
        context = {
            "title": "Register",
            "form": form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserRegisterForm(request.POST or None)
        next_ = request.GET.get('next')

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            login(request, user)
            if next_:
                return redirect(next_)
            return redirect("/")

        context = {
            "title": "Register",
            "form": form
        }
        return render(request, self.template_name, context)


def guest_user_view(request):
    '''
    handle guest user creation\n
    '''
    form = GuestForm(request.POST or None)

    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)

        else:
            return redirect("/users/register/")

    return redirect("/users/register/")
