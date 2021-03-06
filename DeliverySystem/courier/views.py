from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
from django.contrib import messages

from DeliverySystem.models import *
from DeliverySystem.courier import forms


def home(request):
    return redirect(reverse('DeliverySystem:AvailableOrders'))

@login_required(login_url="/sign-in/?next=/delivery/")
def all_jobs_page(request):
    return render(request, 'courier/available_jobs.html', {
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY
    })


@login_required(login_url="/sign-in/?next=/delivery/")
def available_jobs_page(request):
    return render(request, 'courier/available_jobs.html', {
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY
    })

@login_required(login_url="/sign-in/?next=/delivery/")
def available_job_page(request, id):
    job = Job.objects.filter(id=id, status=Job.PROCESSING_STATUS).last()

    if not job:
        return redirect(reverse('DeliverySystem:AvailableOrders'))

    if request.method == 'POST':
        job.courier = request.user.courier
        job.status = Job.PICKING_STATUS
        job.save()

        try:
            layer = get_channel_layer()
            async_to_sync(layer.group_send)("job_" + str(job.id), {
                'type': 'job_update',
                'job': {
                    'status': job.get_status_display(),
                }
            })
        except:
            pass

        return redirect(reverse('DeliverySystem:AvailableOrders'))

    return render(request, 'courier/available_job.html', {
        "job": job
    })

@login_required(login_url="/sign-in/?next=/delivery/")
def current_job_page(request):
    job = Job.objects.filter(
        customer=request.user,
        status__in = [
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).last()

    return render(request, 'courier/current_job.html', {
        "job": job,
        "GOOGLE_MAP_API_KEY": settings.GOOGLE_MAP_API_KEY
    })

@login_required(login_url="/sign-in/?next=/delivery/")
def current_job_take_photo_page(request, id):
    job = Job.objects.filter(
        id=id,
        customer=request.user,
        status__in=[
            Job.PICKING_STATUS,
            Job.DELIVERING_STATUS
        ]
    ).last()
    order = Order.objects.get(job__id=id)

    if not job:
        return redirect(reverse('DeliverySystem:CurrentOrder'))

    return render(request, 'courier/current_job_take_photo.html', {
        "job": job,
        "order": order,
    })

@login_required(login_url="/sign-in/?next=/delivery/")
def job_complete_page(request):
    return render(request, 'courier/job_complete.html')

@login_required(login_url="/sign-in/?next=/delivery/")
def archived_jobs_page(request):
    jobs = Job.objects.filter(
        customer=request.user,
        status=Job.COMPLETED_STATUS
    )

    return render(request, 'courier/archived_jobs.html', {
        "jobs": jobs
    })

@login_required(login_url="/sign-in/?next=/delivery/")
def profile_page(request):
    jobs = Job.objects.filter(
        customer=request.user,
        status=Job.COMPLETED_STATUS
    )

    total_earnings = round(sum(job.price for job in jobs) * 0.8, 2)
    total_jobs = len(jobs)
    total_km = sum(job.distance for job in jobs)

    return render(request, 'courier/profile.html', {
        "total_earnings": total_earnings,
        "total_jobs": total_jobs,
        "total_km": total_km
    })

@login_required(login_url="/sign-in/?next=/courier/")
def payout_method_page(request):
    payout_form = forms.PayoutForm(instance=request.user.courier)

    if request.method == 'POST':
        payout_form = forms.PayoutForm(request.POST, instance=request.user.courier)
        if payout_form.is_valid():
            payout_form.save()

            messages.success(request, "Payout address is updated.")
            return redirect(reverse('DeliverySystem:profile'))

    return render(request, 'courier/payout_method.html', {
        'payout_form': payout_form
    })
