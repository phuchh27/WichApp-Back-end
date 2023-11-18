from .models import Item

class ItemService:
    @staticmethod
    def get_image_link_by_item_id(item_id):
        try:
            item = Item.objects.get(id=item_id)
            return item.image_link
        except Item.DoesNotExist:
            return None
    
    @staticmethod
    def get_store_id_by_item_id(item_id):
        try:
            item = Item.objects.get(id=item_id)
            return item.store_id
        except Item.DoesNotExist:
            # Handle the case where the item is not found
            return None
    
    @staticmethod
    def get_category_id_by_item_id(item_id):
        try:
            item = Item.objects.get(id=item_id)
            return item.category_id
        except Item.DoesNotExist:
            # Handle the case where the item is not found
            return None