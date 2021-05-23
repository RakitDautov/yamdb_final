from rest_framework import serializers

from .models import Review, Comment, Category, Title, Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        exclude = ("title",)

    def validate(self, value):
        """Проверка повторного Review."""
        if self.context.get("request").method == "POST":
            title_id = self.context.get("view").kwargs.get("title_id")
            author = self.context.get("request").user
            if Review.objects.filter(
                title_id=title_id, author=author
            ).exists():
                raise serializers.ValidationError(
                    "Review from that author already exists"
                )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    review = serializers.HiddenField(
        default=serializers.CreateOnlyDefault(None)
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["author"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("id",)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ("id",)


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = "__all__"
        model = Title
        read_only_fields = [
            "rating",
        ]


class TitleSerializerForPostUpdate(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field="slug",
        queryset=Genre.objects.all(),
    )

    class Meta:
        fields = "__all__"
        model = Title
