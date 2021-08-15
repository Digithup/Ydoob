
import hashlib
import os
import os.path
import re
import unicodedata
import zipfile
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.http import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse
)
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.functional import Promise, cached_property
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView, View

import six
from polib import pofile

from . import get_version as get_rosetta_version


#############Rosetta##########
import http
from audioop import reverse
from pydoc import resolve
from urllib.parse import urlsplit, urlunsplit

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, Resolver404, NoReverseMatch
from django.utils.http import is_safe_url
from django.utils.translation import gettext as _, check_for_language, activate, LANGUAGE_SESSION_KEY
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation
# Create your views here.
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

from DNigne import settings
from user.models import User
from localization.models import Home, Language


def all_lang(request):
    lang = Language.objects.all()
    context = {

        'lang': lang,
    }
    return render(request, 'lang-admin.html', context)

class AddLang(CreateView):
    model = Language
    template_name = 'add-lang.html'
    fields = '__all__'

    success_url = reverse_lazy('localization:all_lang')
class EditLang(UpdateView):
    model = Language
    fields = '__all__'
    template_name = 'edit-lang.html'
    success_url = reverse_lazy('localization:all_lang')



class DeleteLang(DeleteView):
    model = Language
    template_name = 'message/confirm_delete.html'
    success_url = reverse_lazy('localization:all_lang')

    def get_object(self, *args, **kwargs):
        obj = super(DeleteLang, self).get_object(*args, **kwargs)

        return obj

def selectlanguage(request):
    if request.method == 'POST':  # check post
        cur_language = translation.get_language()
        lasturl = request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        # return HttpResponse(lang)
        return HttpResponseRedirect(('/') + lang)

@login_required(login_url='/login')  # Check login
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    curren_user = request.user
    language = Language.objects.get(code=request.LANGUAGE_CODE[0:2])
    # Save to User profile database
    data = User.objects.get(user_id=curren_user.id)
    data.language_id = language.id
    data.currency_id = request.session['currency']
    data.save()  # save data
    return HttpResponseRedirect(lasturl)


def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  # check post
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)




 ############################## Rosetta#########################
