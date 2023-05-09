from django.urls import path
from . import views


urlpatterns = [
    path('', views.StoresAPIView.as_view(), name = 'stores'),
    path('<int:id>', views.StoreDetailAPIView.as_view(), name = 'store'),
]
