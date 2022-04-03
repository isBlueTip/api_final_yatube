import logging

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Post, Group, User, Follow
from ..loggers import logger, formatter
from .permissions import IsAuthorOrReadOnly, ReadOnly
from .serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)


LOG_NAME = 'views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class PostViewSet(viewsets.ModelViewSet):
    """Viewset to work with Post model."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        logger.debug('request.data = ')
        logger.debug(request.data)
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid() and isinstance(request.user, User):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to work with Group model."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_permissions(self):
        if self.action == 'retrieve' or self.action == 'list':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset to work with Comment model."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments
        return comments

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowViewSet(viewsets.ModelViewSet):
    """Viewset to work with Follow model."""

    serializer_class = FollowSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        follow = Follow.objects.filter(user=user)
        logger.debug('follow = ')
        logger.debug(follow)
        return follow

    def create(self, request, *args, **kwargs):
        try:
            following = User.objects.get(
                username=request.data.get('following')
            )
        except User.DoesNotExist:
            following = 0
        if not isinstance(following, User):
            return Response(
                'Following must be an existing username',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FollowSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid() and (following != request.user):
            # can't follow myself
            logger.debug(serializer.validated_data)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
