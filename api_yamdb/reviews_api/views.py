import random

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins, status
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import NotFound
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (CategorySerializer, SignUpSerializer,
                          MyTokenObtainPairSerializer, UserSerializer, UserMeSerializer)
from .permissions import IsAuthorOrReadOnlyPermission, AdminOrReadOnly
from reviews.models import User, Category, Genre, Title, Review, Comment

MIN_RANGE = 100000
MAX_RANGE = 999999
STEP = 1

confirmation_code = random.randrange(MIN_RANGE, MAX_RANGE, STEP)


def conformation_send_mail(data):
    send_mail(
        'Тренировка отправки писем',
        f'Код подтверждения: {confirmation_code}',
        'lax@example.com',  # Это поле "От кого"
        [data.get('email')],  # Это поле "Кому" (можно указать список адресов)
        fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
    )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_object(self):
        username = self.kwargs.get('pk')
        if username == 'me':
            return get_object_or_404(User, username=self.request.user.username)
        return get_object_or_404(User, username=username)

    def perform_create(self, serializer):
        res = serializer.save()
        if self.request.method == 'POST':
            user = User.objects.get(username=serializer.data['username'])
            user.set_password(str(confirmation_code))
            user.save()
            conformation_send_mail(self.request.data)
        return res

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UserMeSerializer
        return UserSerializer


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = request.data
        serializer = SignUpSerializer(data=data)
        print(f"User: {User.objects.filter(username=data['username'], email=data['email'])}")
        if serializer.is_valid():
            user = User.objects.create(username=data['username'], email=data['email'])
            print(f'user: {user}__type: {type(user)}')
            user.set_password(str(confirmation_code))
            user.save()
            conformation_send_mail(data)
            return Response(request.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
