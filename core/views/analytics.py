from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render

from sales.models.orders import Order

def OrderByLocation(request):
    #doughnut
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def SalesByLocation(request):
    #pie
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def RevenueByLocation(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def BuyAndSell(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def TotalSales(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def TotalPurchase(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def TotalCashTransaction(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def TotalDeposits(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def MarketValue(request):
    #line
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })







def my_dashboard(request):
    labels = []
    data = []

    orders = Order.objects.all()
    for order in orders:
        labels.append(order.ordered)
        data.append(order.total)

    return render(request, 'analytics/myboard.html', {
        'labels': labels,
        'data': data,
    })


def population_chart(request):
    labels = []
    data = []

    queryset = Order.objects.values('address__address_title').annotate(address_total=Sum('total')).order_by(
        '-address_total')
    for entry in queryset:
        labels.append(entry['address__address_title'])
        data.append(entry['address_total'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
