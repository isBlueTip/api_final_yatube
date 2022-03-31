from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Post, Group, Comment, Follow


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    following = SlugRelatedField(slug_field='username', read_only=True)
    user = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Follow
        fields = ('following', 'user')
