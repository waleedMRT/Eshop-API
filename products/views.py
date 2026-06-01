from django.shortcuts import render , get_object_or_404

from rest_framework import generics , filters , status
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly , IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from.models import Product , Review , Order , OrderItem
from .serializers import ProductSerializer , OrderSerialzer
from .filters import ProductFilter
from .permissions import IsOwnerOrReadOnly




# custom pagination class 
class CustomPagination(PageNumberPagination):
    page_size = 9

# GET ALL PRODUCTS
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer

    # filter 
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter
    ]
    filterset_class = ProductFilter



    #search
    search_fields = ['name' , 'brand' , 'category__name']



    # pagination
    pagination_class = CustomPagination



# POST
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        
        return Response({
            "message" : "added successfuly",
            "product" : serializer.data
        } , status=status.HTTP_201_CREATED)
    
    else:
        return Response( serializer.errors , status=status.HTTP_400_BAD_REQUEST)
    

# GET ONE PRODUCT / DELTE / PUT
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly , IsOwnerOrReadOnly ]


# Reviews

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request , pk):
    user = request.user
    product = get_object_or_404(Product , id=pk)
    data = request.data
    rating = float(data["rating"])
    if product.reviews.filter(user=user).exists():
        return Response({
            'error' : 'Already rated by this user'
        } , status=status.HTTP_400_BAD_REQUEST)
    
    elif rating <= 0 or rating > 5:
        return Response({
            'error' : 'rating must be between 1 and 5'
        } , status=status.HTTP_400_BAD_REQUEST)
    
    review = Review.objects.create(
        user=user,
        product=product,
        rating=rating,
        comment=data.get('comment' , '')
    )
    
    reviews = product.reviews.all()
    product.rating_num = reviews.count()
    total = sum([r.rating for r in reviews])
    product.rating = total / product.rating_num 
    product.save()

    return Response({
        'message' : 'Review added !'
    } , status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    user = request.user
    data = request.data

    order = Order.objects.create(user=user)

    total = 0

    for item in data['items']:
        product = Product.objects.get(id=item['product_id'])

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=product.price
        )

        total += product.price * item['quantity']
    order.totla_price = total
    order.save()

    return Response({
            'message' : 'Order Created Successfuly',
            'order_id' : order.id ,
            'total' : total
        },  status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    count = Order.objects.filter(user=request.user).count
    serializer = OrderSerialzer(
        orders ,
        many=True
    )

    return Response(serializer.data)