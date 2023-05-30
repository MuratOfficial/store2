from django.urls import path

from .views import ProductListView, basket_add, basket_delete

app_name = 'products'

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),
    path('basket_add/<int:product_id>/', basket_add, name='basket_add'),
    path('basket_delete/<int:product_id>/', basket_delete, name='basket_delete'),
]
