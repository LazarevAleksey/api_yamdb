from rest_framework import serializers, validators
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField

from reviews.models import User, Category, Genre, Title, TitleGenre, Review, Comment, Review
from typing import Dict, Any


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=Comment.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
        )
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ("id", "pub_date")
    


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        queryset=Review.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
        )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")
        read_only_fields = ("id", "pub_date", )

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            title_id = self.context['view'].kwargs['title_id']
            title = get_object_or_404(Title, pk=title_id)
            if title.review.filter(author=request.user).exists():
                raise validators.ValidationError(
                    'Пользователь может оставить только один отзыв на произведение.'
                )
        return attrs

    def create(self, validated_data):
        # print(f'validated_data: {validated_data}')
        review = Review.objects.create(**validated_data)
        return review


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CategorySecondSerializer(serializers.ModelSerializer):
    # def validate_empty_values(self, data):
    #     print(f"def validate_empty_values(self, data): {data}")
    #     pass
        
    def to_internal_value(self, data):
        try:
            print(f'category_data: {data}')
            if not isinstance(data, dict):
                data = get_object_or_404(Category, slug=data)
            # print(f'category_data_: {data}')
        except ValueError:
            raise serializers.ValidationError('Неверный формат поля "category"')
        return data

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
    

class GenreSecondSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        try:
            data = get_object_or_404(Genre, slug=data)
            data = {'name': data.name, 'slug': data.slug}
        except ValueError:
            raise serializers.ValidationError('Неверный формат поля "genre"')
        return data
    # def validate_genre(self, value):
    #     print(f'validate_genre_: {value}')
    #     return value

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSecondSerializer(many=True, required=True)
    category = CategorySecondSerializer(required=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    def validate(self, data):
        if not isinstance(data["genre"], list) or not data["genre"]:
            raise serializers.ValidationError(
                'genre - обязательное поле')
        if data['year'] > 2023:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).')
        return data

    def create(self, validated_data):
        genres = validated_data.pop('genre')        
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(
                **genre)
            TitleGenre.objects.create(
                genre=current_genre, title=title)
        return title

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
        if value == 'me':
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
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField(default=None)
        self.fields['confirmation_code'] = serializers.CharField()

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        attrs['password'] = attrs['confirmation_code']
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["token"] = str(refresh.access_token)

        data.pop('refresh', None)
        data.pop('access', None)
        return data
