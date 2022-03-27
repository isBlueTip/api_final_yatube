import logging

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .loggers import logger, formatter
from .permissions import IsAuthorOrReadOnly, ReadOnly
from posts.models import Post, Group
from .serializers import PostSerializer, GroupSerializer, CommentSerializer


LOG_NAME = 'views.log'

file_handler = logging.FileHandler(LOG_NAME)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class PostViewSet(viewsets.ModelViewSet):
    """Viewset to work with Post model."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    permission_classes = [IsAuthorOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        serializer = PostSerializer(
            data=request.data, context={'request': request})
        logger.debug(serializer)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset to work with Group model."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [ReadOnly, ]


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
        logger.debug(serializer)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
