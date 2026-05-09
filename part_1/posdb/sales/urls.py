# sales/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # ── Part 1 views ──────────────────────────────────────
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/mine/', views.my_orders, name='my_orders'),
    path('orders/<int:pk>/cancel/', views.cancel_order, name='cancel_order'),

    # ── Part 2 views (new) ────────────────────────────────
    path('orders/new/', views.create_order, name='create_order'),
    path('orders/<int:pk>/items/', views.add_item, name='add_item'),
]