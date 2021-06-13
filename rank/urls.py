from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('rank/', views.rank),
    
    path('details/', views.details),
    # path('test/', views.search),
    path('search/', views.search),
     path('test/', views.test_render),
    path('', views.rank),
]