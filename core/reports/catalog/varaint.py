from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from tablib import Dataset

from catalog.resources import ProductResource, ColorResource, SizeResource


def colors_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        colors_resource = ColorResource()
        dataset = colors_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="color_export_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="color_export_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="color_export_data.xls"'
            return response

    return render(request, 'catalog/variant/admin-variant.html')

def colors_import_data(request):
    if request.method == 'POST':
        colors_resource = ColorResource()
        dataset = Dataset()
        new_colors = request.FILES['colors-file']

        imported_data = dataset.load(new_colors.read().decode('utf-8'),format='csv')
        result = colors_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            colors_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'catalog/variant/admin-variant.html')


def size_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        size_resource = SizeResource()
        dataset = size_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="size_export_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="size_export_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="size_export_data.xls"'
            return response

    return HttpResponseRedirect(reverse_lazy('core:Variant'))

def size_import_data(request):
    if request.method == 'POST':
        size_resource = SizeResource()
        dataset = Dataset()
        new_colors = request.FILES['colors-file']

        imported_data = dataset.load(new_colors.read().decode('utf-8'),format='csv')
        result = size_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            size_resource.import_data(dataset, dry_run=False)  # Actually import now

    return HttpResponseRedirect(reverse_lazy('core:Variant'))

