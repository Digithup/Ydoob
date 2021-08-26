from django.contrib.auth import get_user_model

#############Rosetta##########

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import translation
# Create your views here.
from django.views.generic import CreateView, UpdateView, DeleteView

from localization.models import Language

#############Rosetta##########

User = get_user_model()
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
