#Archivo de señales para detectar las ordenes creadas

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from .models import Order
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Order)
def nuevaOrden(sender, instance,created, **kwargs):
     if created:
         channel_layer = get_channel_layer()
         try:
             instance.id_cupon != None
             cupon = instance.id_cupon.id
         except:
             cupon = None
             print("No existe cupon")
             
         async_to_sync(channel_layer.group_send)(
             "orders", #Nombre del grupo
             {
                 "type": "nuevaOrden",
                 "order": {
                     "id_order": instance.id_order,
                     "id_cart": instance.id_cart.id,
                     "id_address": instance.id_address.id,
                     "id_cupon": cupon,
                     "id_employee": instance.id_employee.id,
                     "id_status":{
                         "id_status": instance.id_status.id_status,
                         "status": instance.id_status.status,
                     },
                     "order_date": instance.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                     "last_update": instance.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                 }
                 
             }
         )
@receiver(pre_save, sender=Order)
def updateOrderStatus(sender, instance,**kwargs):
        print("se ha actualizado una orden") 
        try:
        #obtener estado antes de guardar
            old_instance = sender.objects.get(id_order=instance.id_order)
            original_Status = old_instance.id_status.id_status
            new_Status = instance.id_status.id_status
            print(f"Original status: {original_Status}, New status: {new_Status}")
            
            #si el estado cambia actualizar el canal
            if original_Status != new_Status:
                print(original_Status)
                print(new_Status)
                channel_layer =  get_channel_layer()
                try:
                    instance.id_cupon != None
                    cupon = instance.id_cupon.id
                except:
                    cupon = None
                    print("No existe cupon")
                async_to_sync(channel_layer.group_send)(
                    "orders", #Nombre del grupo
                    {
                        "type": "updateOrderStatus", #tipo de mensaje para diferenciar
                        "order": {
                            "id_order": instance.id_order,
                            "id_cart": instance.id_cart.id,
                            "id_address": instance.id_address.id,
                            "id_cupon": cupon,
                            "id_employee": instance.id_employee.id,
                            "id_status":{
                                "id_status": instance.id_status.id_status,
                                "status": instance.id_status.status,
                            },
                            "order_date": instance.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                    }
                
                     }

        )
        except Order.DoesNotExist:
            print("No existe la orden")

@receiver(post_save, sender=Order)
def updateOrder(sender, instance,created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        try:
            instance.id_cupon != None
            cupon = instance.id_cupon.id
        except:
            cupon = None
            print("No existe cupon")
        async_to_sync(channel_layer.group_send)(
            "orders", #Nombre del grupo
            {
                "type": "updateOrder",
                "order": {
                    "id_order": instance.id_order,
                    "id_cart": instance.id_cart.id,
                    "id_address": instance.id_address.id,
                    "id_cupon": cupon,
                    "id_employee": instance.id_employee.id,
                    "id_status":{
                        "id_status": instance.id_status.id_status,
                        "status": instance.id_status.status,
                    },
                    "order_date": instance.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "last_update": instance.last_update.strftime('%Y-%m-%d %H:%M:%S'),
                }
                
            })