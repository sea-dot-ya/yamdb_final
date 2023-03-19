from django.contrib import admin

# Register your models here.
from .models import Category, Comments, Genre, GenreTitle, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class GenreAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "slug",
    )
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class CommentsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "author",
        "pub_date",
        "review_id",
    )
    search_fields = (
        "text",
        "author",
    )
    empty_value_display = "-пусто-"


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "text",
        "author",
        "score",
        "pub_date",
        "title_id",
    )
    search_fields = ("title_id",)
    empty_value_display = "-пусто-"


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "year",
        "category",
    )
    search_fields = (
        "name",
        "category",
        "year",
    )
    empty_value_display = "-пусто-"


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = (
        "title_id",
        "genre_id",
    )
    search_fields = (
        "title_id",
        "genre_id",
    )
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
