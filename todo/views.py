from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import viewsets
from .utils import slugify_text
from rest_framework import permissions
from rest_framework.response import Response
from .models import TODOAction, TODOList
from todo import serializers


class TODOListViewSet(viewsets.ViewSet):
    serializer = serializers.TODOSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request):
        user: User = self.request.user
        serializer = serializers.TODOListSerializer(user.todolist, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        user: User = self.request.user
        data = self.request.POST.dict()
        data['slug'] = slugify_text(data.get('title', ''))
        data['user'] = user.pk
        serializer = serializers.TODOListSaveSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)


class TODOViewSet(viewsets.ViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, request) -> TODOList:
        user: User = self.request.user
        todo = user.todolist.filter(slug=self.kwargs['slug'])
        if not todo.exists():
            raise NotFound
        if not todo.filter(user=user).exists():
            raise PermissionDenied('TODO access not granted')
        return todo.get()

    def list(self, request, *args, **kwargs):
        todo = self.get_object(request)
        serializer = serializers.TODOSerializer(todo)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        todo = self.get_object(request)
        data = self.request.POST.dict()
        data['todo'] = todo.pk
        data['slug'] = slugify_text(data.get('title', ''))
        serializer = serializers.TODOActionSaveSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update existing action in todo"""
        todo = self.get_object(request)
        data = self.request.data
        data['slug'] = slugify_text(data.get('title', '') or todo.title)
        serializer = serializers.TODOListSerializer(instance=todo, data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.update(todo, serializer.validated_data)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """Delete existing action in todo"""
        todo = self.get_object(request)
        todo.delete()
        return Response({'status': 'ok'})


class TODOActionViewSet(viewsets.ViewSet):

    def get_object(self) -> TODOList:
        user: User = self.request.user
        action = TODOAction.objects.filter(
            todo__slug=self.kwargs['slug'],
            slug=self.kwargs['action_slug'],
        ).select_related('todo')
        if not action.exists():
            raise NotFound
        if not action.filter(todo__user=user).exists():
            raise PermissionDenied('TODO access not granted')
        return action.get()

    def update(self, request, *args, **kwargs):
        """Create action in todo"""
        action = self.get_object()
        data = self.request.data
        data['slug'] = slugify_text(data.get('title', '') or action.title)
        serializer = serializers.TODOActionSerializer(instance=action, data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.update(action, serializer.validated_data)
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """Delete action in todo"""
        action = self.get_object()
        action.delete()
        return Response({'status': 'ok'})
