from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
    ('8', 8),
    ('9', 9),
    ('10', 10)
)


class Role(models.Choices):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=256,
        choices=Role.choices,
        default=Role.USER
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email', 'username'],
                name='unique_email_username'
            )
        ]

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role=='user'


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    # slug = models.SlugField(unique=True, null=False, blank=False)
    year = models.IntegerField()
    rating = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre'
    )
    category = models.ForeignKey(
        Category,
        # null=False, blank=False,
        # null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='title'
    )

    def __str__(self):
        return self.name
        # return f'{self.name} {self.slug}'


class TitleGenre(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.CharField(max_length=256, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_review',
        verbose_name='Автор отзыва',
    )
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField('pub_date', auto_now_add=True)
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_follow'
            )
        ]

    def __str__(self):
        return f"Отзыв: '{self.text}', автор: '{self.author}'"


class Comment(models.Model):
    text = models.CharField(max_length=256)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment'
    )
