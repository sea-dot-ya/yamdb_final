from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    genre = filters.Filter(field_name="genre__slug")
    category = filters.Filter(field_name="category__slug")

    class Meta:
        model = Title
        fields = ["name", "genre", "category", "year"]
