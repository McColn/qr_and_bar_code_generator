
from django.urls import path,include
from . import views


urlpatterns = [
    
    path('generate-qr/', views.generate_qr, name='generate_qr'),
    path('barCode/', views.barCode, name='barCode'),
    path('barCodeList/', views.barCodeList, name='barCodeList'),
    path('', views.home, name='home'),
]