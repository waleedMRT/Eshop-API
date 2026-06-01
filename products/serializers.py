from rest_framework import serializers
from .models import Product , Category , Order , OrderItem , Review
from cloudinary.utils import cloudinary_url


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'username', 'rating', 'comment', 'created_at']
        

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    user = serializers.StringRelatedField()
    image = serializers.SerializerMethodField()
    reviews = ReviewSerializer(read_only=True , many=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['user']

    def get_image(self , obj):
        if obj.image:
            url , options = cloudinary_url(obj.image.public_id)
            return url
        return ""



class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name' , read_only=True)
    image = serializers.CharField(source='product.image' , read_only=True)
    class Meta:
        model=OrderItem 
        fields = [
            'id',
            'product_name' ,
            'image',
            'quantity',
            'price'
        ]


class OrderSerialzer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True , read_only=True)
    class Meta:
        model = Order
        fields = [
            'id' ,
            'totla_price',
            'created_at',
            'items',
            'is_paid'
        ]