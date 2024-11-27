from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('daraz/', views.select_daraz_product, name='select_daraz_product'),
    path('amazon/', views.select_amazon_product, name='select_amazon_product'),
    path('compare/<int:daraz_id>/<int:amazon_id>/', views.compare_products, name='compare_products'),
]
