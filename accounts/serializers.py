from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

class SignUpserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username' , 'first_name' , 'last_name' , 'email' , 'password'
        ]
        extra_kwargs = {
            'username': {'required': True, 'allow_blank': False},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'email': {'required': True, 'allow_blank': False},
            'password': {
                'required': True,
                'allow_blank': False,
                'min_length': 8,
                'write_only': True  #  مهم: لا يرجع في response
            },
        }

    #  تشفير الباسورد
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    #  منع تكرار الإيميل
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists!")
        return value

class Userserializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id' , 'username' , 'first_name' , 'last_name' , 'email'
        ]