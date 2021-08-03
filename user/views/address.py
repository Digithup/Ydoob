from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from user.forms import UserUpdateAddressForm
from user.models import UserAddress, User


def address_list(request):
    user = User.objects.get(id=request.user.id)
    address = UserAddress.objects.filter(user=user)

    context = {'user': user,
               'address': address,
               }
    return render(request, 'users/user_profile.html', context)


def save_address_form(request, form, template_name):
    data = {}
    user = User.objects.get(id=request.user.id)
    address = UserAddress.objects.filter(user=user)
    if request.method == 'POST':

        if form.is_valid():
            form.instance.user = request.user
            form.save()
            data['form_is_valid'] = True
            address = UserAddress.objects.filter(user=user)

            data['html_book_list'] = render_to_string('users/includes/partial_book_list.html', {
                'address': address
            })
        else:
            data['form_is_valid'] = False
            messages.error(request, "Error")
    context = {'form': form,'address':address}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def CreateAddress(request):
    if request.method == 'POST':
        form = UserUpdateAddressForm(request.POST)
    else:
        form = UserUpdateAddressForm()

    return save_address_form(request, form, 'users/includes/partial_book_create.html')


def UpdateAddress(request, pk):
    address = get_object_or_404(UserAddress, pk=pk)
    if request.method == 'POST':
        form = UserUpdateAddressForm(request.POST, instance=address)
    else:
        form = UserUpdateAddressForm(instance=address)
    return save_address_form(request, form, 'users/includes/partial_book_update.html')


def DeleteAddress(request, pk):
    address = get_object_or_404(UserAddress, pk=pk)
    data = dict()
    if request.method == 'POST':
        address.delete()
        data['form_is_valid'] = True
        address = UserAddress.objects.all()
        data['html_book_list'] = render_to_string('users/includes/partial_book_list.html', {
            'address': address
        })
    else:
        context = {'address': address}
        data['html_form'] = render_to_string('users/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)
