from django.shortcuts import render

from localization.models.models import City, Governorates


def LoadCitiesHelper(request):
    country_id = request.GET.get('country')
    print(country_id)
    governorates = Governorates.objects.filter(country_id=country_id).order_by('name')
    governorates_id = request.GET.get('governorates')
    print(governorates_id)
    cities = City.objects.filter(governorates_id=governorates_id).order_by('name')
    context={
        'governorates':governorates,
        'cities':cities,
    }
    return render(request, 'city_dropdown_list_options.html', context)