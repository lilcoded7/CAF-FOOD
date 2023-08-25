from django.urls import path 
from . import views 


urlpatterns = [
    path('', views.shop, name='food'),
    path('cart/', views.cart, name='cart'), 
    path('navbar/', views.navbar, name='navbar'),
    path('update-item/', views.updateItem, name='update-item'),
    path('process-order/', views.process_order, name='process-order'),
    path('about/', views.about, name='about'),
]   

