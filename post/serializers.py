from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.login', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'text', 'image', 'author', 'author_name',
            'comments', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
