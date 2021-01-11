from django.urls import path
from . import views
from django.conf.urls import include

urlpatterns = [
    path('', views.index),
    path(r'elasticsearchapp/', include('elasticsearchapp.urls')),
]
