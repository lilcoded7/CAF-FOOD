from django.shortcuts import render, redirect, get_object_or_404
from CAFFOOD.models.food import Food 
from CAFFOOD.models.order import Order
from CAFFOOD.models.order_item import OrderItem
from CAFFOOD.models.customer import Customer
from CAFFOOD.models.category import Category
from CAFFOOD.utils import cookie_cart, cartData
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
import json

User = get_user_model()
# Create your views here.


def navbar(request):
    data       = cartData(request)
    items       = data['items']
    order       = data['order']
    total_cart  = data['total_cart'] 
    category = Category.objects.all()
    context = {'category':category, 'total_cart':total_cart}
    return render(request, 'navbar.html', context)

def shop(request):
    data       = cartData(request)
    order       = data['order']
    total_cart  = data['total_cart']
    products = Food.objects.all()
    category = Category.objects.all()
    
    context = {
        'products': products,
        'order': order,
        'total_cart': total_cart,  
        'category':category
    }
    return render(request, 'shop.html', context)


# @login_required
def cart(request):
    data       = cartData(request)
    items       = data['items']
    order       = data['order']
    total_cart  = data['total_cart']
    category = Category.objects.all()
    context = {'items':items, 'order':order,'total_cart':total_cart,'category':category}
    return render(request, 'cart.html', context)

#  add to cart
def updateItem(request):
    data      = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer  = request.user.customer
    product   = Food.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, course=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
         orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()  
    return JsonResponse('Item was added', safe=False)

def about(request):
    data       = cartData(request)
    items       = data['items']
    order       = data['order']
    total_cart  = data['total_cart']
    category = Category.objects.all()
    context = {'items':items, 'order':order,'total_cart':total_cart,'category':category}
    return render(request, 'about.html', context)

def process_order(request):
    data  = json.loads(request.body)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    total   = float(data['shipping']['total'])
    if total == float(order.get_cart_total):
        order.complete = True 
    order.save()
    return JsonResponse('payment complete !', safe=False)

def checkout(request):
    # data       = cartData(request)
    # items       = data['items']
    # order       = data['order']
    # total_cart  = data['total_cart']
    # category = Category.objects.all()
    # context = {'items':items, 'order':order, 'total_cart':total_cart,'category':category}
    return render(request, 'checkout.html', context)



