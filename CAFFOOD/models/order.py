from setup.basemodel import TimeBaseModel
from CAFFOOD.models.customer import Customer
from django.db import models 
import random
import string



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

    def __str__(self):
        return str(self.id) 

    