from django.conf.urls import url
from django.urls import path

from helper.viewHelper import LoadCitiesHelper

app_name = 'helper'

urlpatterns = [



    ##########Address################
    path('helper/ajax/load-cities/', LoadCitiesHelper, name='LoadCitiesHelper'),  # <-- this one here






]
