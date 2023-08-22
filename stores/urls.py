from django.urls import path
from . import views 
from items.views import ItemListCreateAPIView,ItemDetailAPIView


urlpatterns = [
    path('', views.storeListAPIView.as_view(), name = 'Read'),
    path('create/', views.StoresAPIView.as_view(), name = 'Create'),
    path('<int:id>', views.StoreDetailAPIView.as_view(), name = 'store'),
    path('<int:store_id>/items/', ItemListCreateAPIView.as_view(), name='item-list-create'),
    path('<int:store_id>/items/<int:id>/', ItemDetailAPIView.as_view(), name='item-detail'),
    path('categories/', views.CategoriesAPIView.as_view(), name = 'categories'),
    path('paymentcreatestore/', views.StoresPayAPIView.as_view(),name='paymentcreatestore'),   
]
