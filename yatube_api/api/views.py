from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import mixins, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Follow, Group, Post

from .serializers import (CommentSerializer, FollowSerializer,
                          GroupSerializer, PostSerializer)


class BaseViewSet(mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    def author_equal_user(self, data):
        if data.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')

    def perform_update(self, serializer):
        self.author_equal_user(serializer.instance)
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        self.author_equal_user(instance)
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PostViewSet(viewsets.ModelViewSet, BaseViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet, BaseViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.get_post())


class FollowViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                    viewsets.GenericViewSet):

    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', )

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
