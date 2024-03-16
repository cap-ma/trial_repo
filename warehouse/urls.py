from django.urls import path
from .views import WarehouseGetListView

urlpatterns=[
    path("warehouse-product-list/",WarehouseGetListView.as_view(),name='warehouse-get-list')
]
