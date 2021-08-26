from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.http import is_safe_url
from django.views import View
from django.views.generic import CreateView, UpdateView

from user.forms.forms import UserUpdateProfileForm, UserUpdateAddressForm, UserUpdateImageForm, UserRegisterForm, \
    GuestForm
from user.models import GuestEmail, UserAddress

User = get_user_model()


def UserProfile(request, slug):
    user = User.objects.get(id=request.user.id)
    address = UserAddress.objects.filter(user=user)

    context = {'user': user,
               'address': address,
               }
    return render(request, 'users/customers/CustomerProfile.html', context)


def user_delete(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_delete = True
    user.save()
    return redirect('users:user_list')


def UpdateProfile(request, slug):
    user = User.objects.get(id=request.user.id)
    forms = UserUpdateProfileForm(instance=user)
    if request.method == 'POST':
        forms = UserUpdateProfileForm(request.POST, request.FILES, instance=user)
        if forms.is_valid():
            first_name = forms.cleaned_data['first_name']
            last_name = forms.cleaned_data['last_name']
            facebook = forms.cleaned_data['facebook']
            instagram = forms.cleaned_data['instagram']
            twitter = forms.cleaned_data['twitter']
            youtube = forms.cleaned_data['youtube']
            about = forms.cleaned_data['about']
            forms = User.objects.get(id=request.user.id)
            forms.first_name = first_name
            forms.last_name = last_name

            forms.facebook = facebook
            forms.instagram = instagram
            forms.twitter = twitter
            forms.youtube = youtube
            forms.about = about
            forms.save()
            return redirect('user:UserProfile', user.slug)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            messages.error(request, "Error")
    else:
        context = {
            'user': user,
            'forms': forms
        }
        return render(request, 'users/customers/UpdateProfile.html', context)


def UpdateImage(request, slug):
    user = User.objects.get(id=request.user.id)
    forms = UserUpdateImageForm(instance=user)

    if request.method == 'POST':
        forms = UserUpdateImageForm(request.POST, request.FILES, instance=user)
        if forms.is_valid():

            image = request.FILES.get('image')

            forms = User.objects.get(id=request.user.id)

            forms.image = image

            forms.save()
            return redirect('user:UserProfile', user.slug)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            context = {
                'user': user,
                'forms': forms
            }
            return render(request, 'users/customers/user_profile_update_image.html', context)
            messages.error(request, "Error")
    else:
        context = {
            'user': user,
            'forms': forms
        }
        return render(request, 'users/customers/user_profile_update_image.html', context)


def CreateAddress(request, slug):
    user = User.objects.get(id=request.user.id)
    user_address = UserAddress.objects.get(user=user)
    forms = UserUpdateAddressForm()
    context = {
        'user': user,
        'forms': forms
    }
    if request.method == 'POST':
        forms = UserUpdateAddressForm(request.POST, request.FILES, )
        if forms.is_valid():
            address_title = forms.cleaned_data['address_title']
            first_name = forms.cleaned_data['first_name']
            last_name = forms.cleaned_data['last_name']
            governorate = forms.cleaned_data['governorate']
            city = forms.cleaned_data['city']
            area = forms.cleaned_data['area']
            street_name = forms.cleaned_data['street_name']
            location_type = forms.cleaned_data['location_type']
            phone = forms.cleaned_data['phone']
            country = forms.cleaned_data['country']
            shipping_note = forms.cleaned_data['shipping_note']
            building_name = forms.cleaned_data['building_name']
            floor_no = forms.cleaned_data['floor_no']
            apartment_no = forms.cleaned_data['apartment_no']
            nearest_landmark = forms.cleaned_data['nearest_landmark']
            postal_code = forms.cleaned_data['postal_code']
            print(request)
            forms = UserAddress(address_title=address_title, first_name=first_name, last_name=last_name,
                                governorate=governorate, city=city, area=area, street_name=street_name,
                                location_type=location_type, phone=phone, country=country,
                                shipping_note=shipping_note, user=user,
                                building_name=building_name, floor_no=floor_no, apartment_no=apartment_no,
                                nearest_landmark=nearest_landmark,
                                postal_code=postal_code)

            forms.save()
            messages.success(request, "SUCCESS")
            # return HttpResponseRedirect("pk")
            # return render(request, 'users/CustomerProfile.html')
            return redirect('user:UserProfile', user.slug)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            messages.error(request, "Error")
    else:
        user = User.objects.get(id=request.user.id)
        forms = UserUpdateAddressForm()
        context = {
            'user': user,
            'forms': forms,
            'user_address': user_address
        }
        return render(request, 'users/customers/UpdateAddress.html', context)
    context = {
        'user': user,
        'forms': forms,
        'user_address': user_address,
    }
    return render(request, 'users/customers/UpdateAddress.html', context)


def address_create(request):
    data = dict()
    user = User.objects.get(id=request.user.id)
    user_address = UserAddress.objects.get(user=user)
    if request.method == 'POST':
        form = UserUpdateAddressForm(request.POST)
        if form.is_valid():
            form = UserAddress(user=user)
            form.save()
            data['form_is_valid'] = True
            address = UserAddress.objects.all()
            data['html_book_list'] = render_to_string('users/includes/partial_book_list.html', {
                'address': address
            })
        else:
            data['form_is_valid'] = False
    else:
        form = UserUpdateAddressForm()

    context = {'form': form}
    data['html_form'] = render_to_string('users/includes/partial_book_create.html',
                                         context,
                                         request=request
                                         )
    return JsonResponse(data)


def UpdateAddress(request, slug):
    user = User.objects.get(id=request.user.id)
    user_address = UserAddress.objects.get(user=user)
    forms = UserUpdateAddressForm()
    context = {
        'user': user,
        'forms': forms
    }
    if request.method == 'POST':
        forms = UserUpdateAddressForm(request.POST, request.FILES, )
        if forms.is_valid():
            address_title = forms.cleaned_data['address_title']
            first_name = forms.cleaned_data['first_name']
            last_name = forms.cleaned_data['last_name']
            governorate = forms.cleaned_data['governorate']
            city = forms.cleaned_data['city']
            area = forms.cleaned_data['area']
            street_name = forms.cleaned_data['street_name']
            location_type = forms.cleaned_data['location_type']
            phone = forms.cleaned_data['phone']
            country = forms.cleaned_data['country']
            shipping_note = forms.cleaned_data['shipping_note']
            building_name = forms.cleaned_data['building_name']
            floor_no = forms.cleaned_data['floor_no']
            apartment_no = forms.cleaned_data['apartment_no']
            nearest_landmark = forms.cleaned_data['nearest_landmark']
            postal_code = forms.cleaned_data['postal_code']
            print(request)
            forms = UserAddress(address_title=address_title, first_name=first_name, last_name=last_name,
                                governorate=governorate, city=city, area=area, street_name=street_name,
                                location_type=location_type, phone=phone, country=country,
                                shipping_note=shipping_note, user=user,
                                building_name=building_name, floor_no=floor_no, apartment_no=apartment_no,
                                nearest_landmark=nearest_landmark,
                                postal_code=postal_code)

            forms.save()
            messages.success(request, "SUCCESS")
            # return HttpResponseRedirect("pk")
            # return render(request, 'users/CustomerProfile.html')
            return redirect('user:UserProfile', user.slug)
        else:
            print("Form invalid, see below error msg")
            print(request.POST)
            messages.error(request, "Error")
    else:
        user = User.objects.get(id=request.user.id)
        forms = UserUpdateAddressForm()
        context = {
            'user': user,
            'forms': forms,
            'user_address': user_address
        }
        return render(request, 'users/customers/UpdateAddress.html', context)
    context = {
        'user': user,
        'forms': forms,
        'user_address': user_address,
    }
    html_form = render_to_string('users/customers/UpdateAddress.html',
                                 context,
                                 request=request,
                                 )
    return JsonResponse({'html_form': html_form})


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
