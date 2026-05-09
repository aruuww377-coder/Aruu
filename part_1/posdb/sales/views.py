# sales/views.py

from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem
from .forms import OrderItemForm


@login_required
def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'sales/product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'sales/product_detail.html', {'product': product})


@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'sales/order_list.html', {'orders': orders})


@login_required
def my_orders(request):
    orders = Order.objects.filter(cashier=request.user)
    return render(request, 'sales/order_list.html', {'orders': orders})


@login_required
def create_order(request):
    order = Order.objects.create(
        cashier=request.user,
        status='open',
    )
    return redirect('add_item', pk=order.pk)


@login_required
def add_item(request, pk):
    order = get_object_or_404(Order, pk=pk)

    # Prevent adding items if order is not open
    if order.status != 'open':
        messages.error(request, 'This order is cancelled.')
        return redirect('order_list')

    if request.method == 'POST':

        # Mark order as paid
        if 'mark_paid' in request.POST:
            order.status = 'paid'
            order.save()
            return redirect('order_list')

        item_form = OrderItemForm(request.POST)

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.order = order
            item.unit_price = item.product.price
            item.save()

            # Deduct stock
            product = item.product
            product.stock -= item.quantity
            product.save()

            return redirect('add_item', pk=order.pk)

    else:
        item_form = OrderItemForm()

    return render(request, 'sales/add_item.html', {
        'order': order,
        'item_form': item_form,
        'items': order.items.select_related('product'),
    })


@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if order.status == 'cancelled':
        messages.info(request, 'Order is already cancelled.')
        return redirect('order_list')

    with transaction.atomic():
        for item in order.items.select_related('product'):
            product = item.product
            product.stock += item.quantity
            product.save()

        order.status = 'cancelled'
        order.save()

    messages.success(request, 'Order cancelled and stock restored.')
    return redirect('order_list')