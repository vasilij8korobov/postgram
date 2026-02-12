from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.login', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'author', 'author_name', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
