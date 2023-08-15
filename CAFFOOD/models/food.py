from setup.basemodel import TimeBaseModel
from CAFFOOD.models.category import Category
from django.db import models 


class Food(TimeBaseModel):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    was_price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    charges = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True, default=0)
    image = models.ImageField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True) 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    @property 
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url 

    @property 
    def videoURL(self):
        try:
            url = self.video.url
        except:
            url = ''
        return url 

    def __str__(self):
        return self.name 
