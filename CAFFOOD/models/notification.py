from django.db import models


class Notification(models.Model):
    head = models.CharField(max_length=20)
    message =  models.CharField(max_length=100)

    def __str__(self):
        return self.head