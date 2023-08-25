from CAFFOOD.models.food import Food 
from CAFFOOD.models.order import Order
from CAFFOOD.models.order_item import OrderItem
from CAFFOOD.models.customer import Customer
from django.http import JsonResponse
import json



# Ananymous user add to cart 
def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    total_cart = order['get_cart_items']

    for i in cart:  
        try:   
            total_cart += cart[i]['quantity']

            product = Food.objects.get(id=i)
            total   = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product' : {
                    'id': product.id,
                    'name':product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                    },
                'quantity':cart[i]['quantity'],
                'get_total':total,
            }
            items.append(item)
        except:
            pass 
    return {'items':items, 'order':order,'total_cart':total_cart}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total_cart = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        items       = cookie_data['items']
        order       = cookie_data['order']
        total_cart  = cookie_data['total_cart']
    return {'items':items, 'order':order,'total_cart':total_cart}

def generate_random_code():
    # Generate a random pin consisting of five digits
    return ''.join(random.choices(string.digits, k=5))


def generate_qr_code(self):
    # Create a string representing the order details for the QR code
    order_info = generate_random_code
    # Generate the QR code image
    qr = QRCode(
        version=1,
        error_correction=QRCodeOptions.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(order_info)
    qr.make(fit=True)
    # Create an image from the QR code
    qr_image = qr.make_image(fill_color="black", back_color="white")
    # Convert the image to PNG format
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    return qr_image
