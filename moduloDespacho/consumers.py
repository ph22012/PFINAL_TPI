import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Order, Order_status
from channels.db import database_sync_to_async

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        #Coneccion a un grupo de webSocket llamado 'orders'
        self.group_name = 'orders'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        #salir del grupo de webSocket llamado 'orders'
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    #Metodo para enviar las ordenes a los conectados
    async def nuevaOrden(self, event):
        order = event['order']
        await self.send(text_data=json.dumps({
            "type": "NuevaOrden",
            "order": order
            
        }))
    
    async def updateOrderStatus(self, event):
        order = event['order']
        await self.send(text_data=json.dumps({
            "type": "updateOrderStatus",
            "order": order
            
        }))
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        tipo = data['type']
        if tipo == "procesarOrden":
            id_orden = data['idOrden']
            await self.procesarOrden(id_orden)
            
            
    @database_sync_to_async
    def procesarOrden(self, id_orden):
        try:
            next_status = Order_status.objects.get(id_status=2)
            order = Order.objects.get(id_order=id_orden)
            order.id_status = next_status
            order.save()
        except Order.DoesNotExist:
            print("No existe la orden")
        