
from django.urls import path
from .views import SelectItemByCategoryAPIView

urlpatterns = [
    path('items/<int:store_id>/<int:category_id>/', SelectItemByCategoryAPIView.as_view(), name='item-list'),
]
