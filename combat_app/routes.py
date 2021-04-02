from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('info', views.info),
    path('select', views.select),
    path('fight_start', views.fight_start),
    path('fight', views.fight),
    path('fight_advance', views.fight_advance),
    path('result', views.result),


]
