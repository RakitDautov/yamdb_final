from django.contrib import admin

from .models import Review, Comment, Title, Genre, Category


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "text", "author", "score", "pub_date")
    search_fields = ("author", "text")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "review", "text", "author", "pub_date")
    search_fields = (
        "author",
        "text",
    )


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "year", "description", "category")
    search_fields = (
        "name",
        "category",
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
