from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('getdistrict', views.getdistrict, name="getdistrict"),
    path('states-and-districts', views.states_districts,
         name="states_and_districts"),
    path('runscript', views.runscript, name="runscript"),
]
