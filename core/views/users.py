from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import is_safe_url
from django.views import View
from django.views.generic import UpdateView, CreateView, ListView, DetailView, DeleteView

from user.admin import User
from user.forms import UserAdminChangeForm, UserLoginForm, UserRegisterForm
from user.signals import user_logged_in


class AdminLogin(View):
    """
    Description:Will be used to login and logout users.\n
    """
    template_name = 'admin/login.html'

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
                    return redirect("/admin/")

            else:
                print("error")
                return redirect("/admin/login/")

        context = {
            "title": "Login",
            "form": form
        }
        return render(request, self.template_name, context)


def AdminLogout(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse_lazy("accounts:AdminLogin"))


class AdminUsersList(ListView):
    model = User
    template_name = 'users/admin-user-list.html'
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AdminUserDetail(DetailView):
    model = User
    template_name = 'users/admin-user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class AdminUserCreate(View):
    """
    Description:View to create a new user.\n
    """
    template_name = 'users/admin-user-create.html'

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


class AdminUserEdit(UpdateView):
    model = User
    fields = '__all__'
    template_name = 'users/admin-user-edit.html'
    success_url = reverse_lazy('core:AdminUsersList')


class AdminUserDelete(DeleteView):
    model = User
    fields = '__all__'
    success_url = reverse_lazy('core:AdminUsersList')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
