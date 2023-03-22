import api.serializers as ser
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, GenreTitle, Review, Title

from .filters import TitleFilter
from .perrmissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrReadOnly
from .utils import generate_mail

# Isort отрабатывает, мы так и сортировали по isort,
# Но вы говорите что это не правильно, как нам быть, время идет
# Новый спринт стартанул, а мы все с ипортами бьемся,
# которые еще и не понятно как отрабатывают

User = get_user_model()


class GetPostDelViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class GetPostDelPatchViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    pass


@api_view(["POST"])
def code_confirmation(request):
    serializer = ser.SignUpSerializer(data=request.data)

    existing_user = User.objects.filter(
        username=request.data.get("username")
    ).first()
    if existing_user and existing_user.email == request.data.get("email"):
        generate_mail(existing_user)
        return Response(request.data, status=status.HTTP_200_OK)

    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    generate_mail(user)
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    from rest_framework import status

    serializer = ser.AuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data["username"]
    )
    confirmation_code = serializer.validated_data["confirmation_code"]
    token = default_token_generator.check_token(user, confirmation_code)

    if token == confirmation_code:
        jwt_token = RefreshToken.for_user(user)
        return Response(
            {"Ваш токен:": f"{jwt_token}"}, status=status.HTTP_200_OK
        )
    return Response({"Доступ запрещен!"}, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(GetPostDelViewset):
    queryset = Category.objects.all()
    serializer_class = ser.CategorySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = (
        "name",
        "slug",
    )
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("^name",)
    lookup_field = "slug"


class GenreViewSet(GetPostDelViewset):
    queryset = Genre.objects.all()
    serializer_class = ser.GenreSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = (
        "name",
        "slug",
    )
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("^name",)
    lookup_field = "slug"


class GenreTitleViewSet(viewsets.ModelViewSet):
    queryset = GenreTitle.objects.all()
    serializer_class = ser.GenreTitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ("POST", "PATCH"):
            return ser.TitlePostSerializer
        return ser.TitleReadSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("pk")
    serializer_class = ser.UserSerializer
    filter_backends = [filters.SearchFilter]
    lookup_field = "username"
    search_fields = [
        "username",
    ]
    permission_classes = (IsAuthenticated, IsAdmin)
    http_method_names = ("get", "post", "head", "patch", "delete")

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        if request.method == "GET":
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.serializer_class(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop("role", None)
        serializer.update(request.user, serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = ser.CommentsSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(review=review, author=self.request.user)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ser.ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(title=title, author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()
