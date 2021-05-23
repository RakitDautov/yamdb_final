from django_filters.rest_framework import FilterSet, CharFilter

from api.models import Title


class TitleFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Title
        fields = ["name", "year"]

    def filter_queryset(self, queryset):
        genre_slug = self.request.query_params.get("genre", None)
        category_slug = self.request.query_params.get("category", None)

        if genre_slug is not None:
            queryset = queryset.filter(genre__slug=genre_slug)
        if category_slug is not None:
            queryset = queryset.filter(category__slug=category_slug)

        return super().filter_queryset(queryset)
