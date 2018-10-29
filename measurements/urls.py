from django.urls import path
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url('^$', views.index),
    url(r'^measurements/', views.MeasurementList),
    url(r'^thresholds/', views.ThresholdList, name='thresholdList'),
    url(r'^threshold/(?P<id_threshold>\d+)/$', views.ThresholdEdit, name='thresholdEdit'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^', include('social_django.urls')),
]