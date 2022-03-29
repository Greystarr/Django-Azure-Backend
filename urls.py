from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poll/',views.poll_list),
    path('resource-group/',views.getRG),
    path('resource/',views.getResource),
    path('secret/',views.getSecret),
    path('billing/',views.billing),
]