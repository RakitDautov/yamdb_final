from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import (PageNumberPagination)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .filters import TitleFilter
from .models import Category, Genre, Title, Review
from .permissions import (IsAuthorOrAdminOrModeratorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleSerializer, TitleSerializerForPostUpdate,
                          ReviewSerializer, CommentSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrAdminOrModeratorOrReadOnly]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get("review_id"),
                                   title_id=self.kwargs.get("title_id"))

        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        serializer.save(author=self.request.user, review=review)


class BasicViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    pass


class CategoryViewSet(BasicViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(BasicViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = PageNumberPagination
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return TitleSerializerForPostUpdate
        else:
            return self.serializer_class
