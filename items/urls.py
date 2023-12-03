
from django.urls import path
from .views import ItemCategoryListCreateAPIView, ItemCategoryRetrieveUpdateDestroyAPIView, SelectItemByCategoryAPIView,GetItemsByStoreId,ItemUpdateAPIView

urlpatterns = [
    path('items/<int:store_id>/<int:category_id>/', SelectItemByCategoryAPIView.as_view(), name='item-list'),
    path('items/<int:store_id>/staff/', GetItemsByStoreId.as_view(), name='get_items_by_store_id'),
    path('update/<int:id>/', ItemUpdateAPIView.as_view(), name='update_item'),
    path('stores/<int:store_id>/categories/', ItemCategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('stores/<int:store_id>/categories/<int:pk>/', ItemCategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-retrieve-update-destroy'),
]
