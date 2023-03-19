from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-id"]


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-id"]


class Title(models.Model):
    """Подель произведений"""

    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="category",
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through="GenreTitle")

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["-id"]


class ReviewCommentModel(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-pub_date",)

    def __str__(self):
        return self.text[:20]


class Review(ReviewCommentModel):
    """Модель отзывов"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    score = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta(ReviewCommentModel.Meta):
        unique_together = [
            "author",
            "title",
        ]


class Comments(ReviewCommentModel):
    """Модель комментариев"""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
    )


class GenreTitle(models.Model):
    """Модель жанров произведения"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="genre_title",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="genre_title",
    )

    def __str__(self) -> str:
        return self.title.name
