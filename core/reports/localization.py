from django.shortcuts import render
from django.http import HttpResponse
from tablib import Dataset


from localization.resources import GovernoratesResource, CityResource, AreaResource, CountryResource


def country_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        country_resource = CountryResource()
        dataset = country_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="country_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="country_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="country_data.xls"'
            return response
        elif file_format == 'Choose format...':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="country_data.xls"'
            return response



    return render(request, 'localization/country/admin-country.html')

def country_import_data(request):
    if request.method == 'POST':
        country_resource = CountryResource()
        dataset = Dataset()
        new_country = request.FILES['country-file']

        imported_data = dataset.load(new_country.read().decode('utf-8'), format='csv')
        result = country_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            country_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'catalog/variant/admin-variant.html')

def governorates_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        governorates_resource = GovernoratesResource()
        dataset = governorates_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="governorates_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="governorates_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="governorates_data.xls"'
            return response
        elif file_format == 'Choose format...':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="governorates_data.xls"'
            return response

    return render(request, 'localization/country/admin-country.html')


def governorates_import_data(request):
    if request.method == 'POST':
        person_resource = GovernoratesResource()
        dataset = Dataset()
        new_persons = request.FILES['governorates-file']

        imported_data = dataset.load(new_persons.read().decode('utf-8'),format='csv')
        result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'localization/country/admin-country.html')


def city_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        city_resource = CityResource()
        dataset = city_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="city_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="city_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="city_data.xls"'
            return response

    return render(request, 'localization/country/admin-country.html')
def city_import_data(request):
    if request.method == 'POST':
        city_resource = CityResource()
        dataset = Dataset()
        new_persons = request.FILES['city-file']
        print(request)
        imported_data = dataset.load(new_persons.read().decode('utf-8'),format='csv')
        result = city_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            city_resource.import_data(dataset, dry_run=False)  # Actually import now
            print(request.POST)

    return render(request, 'localization/country/admin-country.html')


def area_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        area_resource = AreaResource()
        dataset = area_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="area_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="area_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="area_data.xls"'
            return response

    return render(request, 'localization/country/admin-country.html')

def area_import_data(request):
    if request.method == 'POST':
        area_resource = AreaResource()
        dataset = Dataset()
        new_persons = request.FILES['area-file']
        print(request)
        imported_data = dataset.load(new_persons.read().decode('utf-8'), format='csv')
        result = area_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            area_resource.import_data(dataset, dry_run=False)  # Actually import now
            print(request.POST)

    return render(request, 'localization/country/admin-country.html')