from django.db.models.signals import post_save 
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from CAFFOOD.models.order import Order
from CAFFOOD.utils import notification
from account.utils import EmailSender

User = get_user_model()

@receiver(post_save, sender=Order)
def create_user_notification(sender, instance, created, **kwargs):
    if created:
        head = 'CAF | FOOD'
        message = 'Order is successful, kindly visit Uenr Cafiteria for your order' 
        notification(head, message)
        EmailSender().send_notification_email(instance.customer.email)


@receiver(post_save, sender=User)
def create_user_notification(sender, instance, created, **kwargs):
    if created:
        head = 'CAF | FOOD'
        message = 'Your registration successfully' 
        notification(head, message)
        EmailSender().send_notification_email(instance.customer.email)