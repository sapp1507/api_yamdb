from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review

    def max_one_review(self, data):
        title_id = self.context["request"].parser_context["kwargs"]["title_id"]
        title = get_object_or_404(Title, pk=title_id)
        user = self.context["request"].user
        if (
            self.context["request"].method == "POST"
            and Review.objects.filter(author=user, title=title).exists()
        ):
            raise ParseError("Нельзя оставлять более одного отзыва на произведение."
                             "Но можно изменить существующий")
        return data
