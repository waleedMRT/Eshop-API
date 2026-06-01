import django_filters
from .models import Product ,Category

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    brand= django_filters.CharFilter(lookup_expr='iexact')
    price = django_filters.NumberFilter(lookup_expr='iexact')
    min_price = django_filters.NumberFilter(lookup_expr='gte' , field_name='price')
    max_price = django_filters.NumberFilter(lookup_expr='lte' , field_name='price')

    class Meta:
        model = Product
        fields = ['brand' , 'category' , 'name' , 'min_price' , 'max_price']