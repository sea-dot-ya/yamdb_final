import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comments, Genre, GenreTitle, Review, Title

from .validators import username_validation

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    def validate_username(self, value):
        return username_validation(self, value)

    class Meta:
        fields = ("username", "email")
        model = User


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=100)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreTitle
        exclude = ("id",)


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = "__all__"


class TitlePostSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=False)
    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
        default=CategorySerializer(required=True),
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        slug_field="slug",
        default=GenreSerializer(required=True),
    )

    def validate_year(self, value):
        year = datetime.datetime.today().year
        if value > year:
            raise serializers.ValidationError(
                "Год выпуска не может быть выше текущего"
            )
        return value

    class Meta:
        model = Title
        fields = "__all__"


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ("id", "review", "text", "author", "pub_date")
        read_only_fields = ("author", "review", "pub_date")

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ("id", "title", "text", "author", "score", "pub_date")
        read_only_fields = ("author", "title", "pub_date")

    def validate(self, data):
        title = get_object_or_404(
            Title, pk=self.context["view"].kwargs.get("title_id")
        )
        request = self.context["request"]
        if request.method == "POST":
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise serializers.ValidationError("Отзыв уже оставлен!")
        return data

    def create(self, validated_data):
        return Review.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        return username_validation(self, value)

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "role",
            "email",
        )
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    def validate_username(self, value):
        return username_validation(self, value)

    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "role",
            "email",
        )
        model = User
