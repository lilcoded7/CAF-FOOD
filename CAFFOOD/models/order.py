from setup.basemodel import TimeBaseModel
from CAFFOOD.models.customer import Customer
from django.db import models 
import qrcode
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify

class Order(TimeBaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    received = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    qr_code = models.ImageField(blank=True, null=True)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total      = sum([item.get_total for item in orderitems])
        return total 
        
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total      = sum([item.quantity for item in orderitems])
        return total 

    def status(self):
        self.complete=True
        self.received=True
        self.save()
        

    def generate_qr_code(self):
        order_info = f"\nCustomer: {self.customer.name}\nOrder: {self.received}\nstatus: received"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(order_info)
        qr.make(fit=True)
        
        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        
        image_name = f"qr_code_{slugify(order_info)}.png"
        self.qr_code.save(image_name, ContentFile(buffer.getvalue()))
        self.save()


    def __str__(self):
        return str(self.id) 

    