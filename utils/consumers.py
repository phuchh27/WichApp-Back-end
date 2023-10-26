import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer



class ItemConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        from items.models import Item
        from items.serializers import ItemSocketSerializer
        
        data = json.loads(text_data)
        store_id = data.get('store_id', None)

        if store_id is not None:
            items = Item.objects.filter(store_id=store_id)
            items_list = [ItemSocketSerializer(item).data for item in items]
            await self.send(text_data=json.dumps({'items': items_list}))
