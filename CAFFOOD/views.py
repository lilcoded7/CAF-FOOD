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
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.db.models import DecimalField 
import json
import cv2


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

@login_required
def cart(request):
    data       = cartData(request)
    items       = data['items']
    order       = data['order']
    total_cart  = data['total_cart']
    category = Category.objects.all()
    context = {'items':items, 'order':order,'total_cart':total_cart,'category':category}
    return render(request, 'cart.html', context)

def updateItem(request):
    data      = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer  = request.user.customer
    product   = Food.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, food=product)
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
        order.status()
        order.generate_qr_code()
        order.get_order_total_price()
    order.save()
    return JsonResponse('payment complete !', safe=False)

@login_required
def receipt(request, pk):
    user = request.user 
    qr_code = get_object_or_404(Order, customer__user=user, complete=True, id=pk)
    return render(request, 'qrcode.html', {'qr_code':qr_code})

@login_required
def dashboard(request):
    user = request.user 
    orders = Food.objects.filter(orderitem__order__complete=True, orderitem__order__customer__user=user).count()
    order_food = OrderItem.objects.filter(order__complete=True, order__customer__user=user)
    context = {'orders':orders, 'order_food':order_food}
    return render(request, 'dashboard.html', context)

def read_qr_code(request):
    if request.method == 'POST':
        image = request.FILES['image'].read()
        image = np.asarray(bytearray(image), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        qr_code_detector = cv2.QRCodeDetector()
        retval, decoded_info, points, _ = qr_code_detector.detectAndDecode(gray)

        if retval:
            response_data = {
                'message': 'QR Code detected',
                'decoded_info': decoded_info,
                'qr_code_points': points.tolist(),
            }
        else:
            response_data = {
                'message': 'No QR Code detected in the image.',
            }

        return JsonResponse(response_data)

    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def admin_dashboard(request):
    orders = Order.objects.filter(complete=True).count()
    order_price = Order.objects.aggregate(total=Coalesce(Sum('order_price'), Value(0, output_field=DecimalField())))
    total_order_price = order_price['total']
    order_items = OrderItem.objects.filter(order__complete=True)
    return render(request, 'admin.html', {'orders':orders, 'order_items':order_items, 'total_order_price':total_order_price})
    