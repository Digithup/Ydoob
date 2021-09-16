from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from tablib import Dataset

from catalog.resources import ProductResource


def products_export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']

        product_resource = ProductResource()
        dataset = product_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="products_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="products_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="products_data.xls"'
            return response

    return HttpResponseRedirect(reverse_lazy('core:ProductsList'))


def products_import_data(request):
    if request.method == 'POST':
        product_resource = ProductResource()
        dataset = Dataset()
        new_colors = request.FILES['products-file']

        imported_data = dataset.load(new_colors.read().decode('utf-8'),format='csv')
        result = product_resource.import_data(dataset, dry_run=True)  # Test the data import

        if not result.has_errors():
            product_resource.import_data(dataset, dry_run=False)  # Actually import now

    return HttpResponseRedirect(reverse_lazy('core:ProductsList'))