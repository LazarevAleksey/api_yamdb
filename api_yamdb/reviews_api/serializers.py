from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import User, Category
from typing import Dict, Any


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username']
            )
        ]


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio')

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username']
            )
        ]


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate_username(self, value):
        if value=='me':
            raise serializers.ValidationError("Использовать имя 'me' в качестве username запрещено!")
        return value

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['email', 'username']
            )
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(f'self.fields: {self.fields}')
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(default=None)
        # self.fields['password'].required = False
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        attrs['password'] = attrs['confirmation_code']
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["token"] = str(refresh.access_token)

        data.pop('refresh', None)
        data.pop('access', None)
        return data








