import logging

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Post, Group, User, Comment, Follow
from .loggers import logger, formatter
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
    # queryset = Follow.objects.all()

    def get_queryset(self):
        user = self.request.user
        follow = Follow.objects.filter(user=user)
        logger.debug('follow = ')
        logger.debug(follow)
        return follow

    # def list(self, request, *args, **kwargs):
    #     # user = request.user
    #
    #     # serializer = FollowSerializer(
    #     #     data=request.data, context={'request': request})
    #
    #     serializer = self.get_serializer()
    #
    #     logger.debug('serializer = ')
    #     logger.debug(serializer)
    #     if serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def list(self, request, *args, **kwargs):
    #     logger.debug('request.data = ')
    #     logger.debug(request.data)
    #     logger.debug(type(request.data))
    #
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #
    #         logger.debug('serializer = ')
    #         logger.debug(serializer)
    #         logger.debug(type(serializer))
    #         return self.get_paginated_response(serializer.data)
    #
    #     serializer = self.get_serializer(queryset, many=True)
    #
    #     logger.debug('serializer = ')
    #     logger.debug(serializer)
    #     logger.debug(type(serializer))
    #     return Response(serializer.data)
