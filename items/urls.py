
from django.urls import path
from .views import SelectItemByCategoryAPIView,GetItemsByStoreId

urlpatterns = [
    path('items/<int:store_id>/<int:category_id>/', SelectItemByCategoryAPIView.as_view(), name='item-list'),
    path('items/<int:store_id>/staff/', GetItemsByStoreId.as_view(), name='get_items_by_store_id'),
]
