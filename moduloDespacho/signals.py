#Archivo de señales para detectar las ordenes creadas

from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Order)
def nuevaOrden(sender, instance,created, **kwargs):
     if created:
         channel_layer = get_channel_layer()
         async_to_sync(channel_layer.group_send)(
             "orders", #Nombre del grupo
             {
                 "type": "nuevaOrden",
                 "order": {
                     "id_order": instance.id_order,
                     "id_cart": instance.id_cart,
                     "id_address": instance.id_address,
                     "id_cupon": instance.id_cupon,
                     "id_employee": instance.id_employee,
                     "id_status": instance.id_status.id_status,
                     "order_date": instance.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                 }
                 
             }
         )