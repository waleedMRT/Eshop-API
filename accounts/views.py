from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status
from .serializers import SignUpserializer , Userserializer
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register(request):
    serializer = SignUpserializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message" : "Account created successfuly"
        } , status=status.HTTP_201_CREATED)
        
    else:
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = Userserializer(request.user)
    return Response(serializer.data)