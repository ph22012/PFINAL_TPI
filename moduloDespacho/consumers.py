import json
from channels.generic.websocket import AsyncWebsocketConsumer
#from django.forms.models import model_to_dict

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
            "order": order
            
        }))
        