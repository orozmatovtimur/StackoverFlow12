from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from main.models import *
from main.permissions import IsAuthorPermission
from main.serializers import ProblemSerializer, ReplySerializer, CommentSerializer


class PermissionMixin:  # TODO: узнать побольше про это, что за баг про только одного юзера
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated,] # TODO: почему передаем в списке?
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission,]
        else:
            permissions = []
        return [permission() for permission in permissions ] # list comprehension
                # как мы вызываем permission, это же не функция?


# тут миксины
class ProblemViewSet(PermissionMixin, ModelViewSet):
    # when working with DRF we write queryset, not model
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    # http_method_names = ['GET', 'POST', 'PUT', 'DELETE']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class ReplyViewSet(PermissionMixin, ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer











