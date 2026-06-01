from django.urls import path
from .views import ProductListView , ProductDetailView , add_product , add_review  , create_order , my_orders
urlpatterns = [
    path('products/' , ProductListView.as_view() , name='products' ),
    path('products/<int:pk>' , ProductDetailView.as_view() , name='product_details'),
    path('products/add/' , add_product , name='add_product'),
    path('products/<int:pk>/reviews/' , add_review , name='add_review'),
    path('products/create_order/' , create_order , name='create_order'),
    path('products/my_orders/' , my_orders , name='my_orders')
]