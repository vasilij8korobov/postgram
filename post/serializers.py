from rest_framework import serializers
from .models import Post
from .services import PostService


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.login', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'text', 'image', 'author', 'author_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        author = self.context['request'].user
        return PostService.create_post(validated_data, author)
