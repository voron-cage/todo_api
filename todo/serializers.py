from .models import TODOList, TODOAction
from rest_framework import serializers


class TODOListSerializer(serializers.ModelSerializer):
    action_count = serializers.SerializerMethodField()

    def get_action_count(self, obj: TODOList):
        return obj.todo_action.count()

    class Meta:
        model = TODOList
        fields = ['id', 'title', 'slug', 'created', 'updated', 'order', 'action_count']


class TODOListSaveSerializer(TODOListSerializer):

    class Meta:
        model = TODOList
        fields = TODOListSerializer.Meta.fields + ['user']


class TODOActionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TODOAction
        fields = ['id', 'title', 'is_done', 'slug', 'expire_time', 'created', 'updated', 'order']


class TODOActionSaveSerializer(TODOActionSerializer):

    class Meta:
        model = TODOAction
        fields = TODOActionSerializer.Meta.fields + ['todo']


class TODOSerializer(serializers.ModelSerializer):
    action_count = serializers.SerializerMethodField()
    actions = TODOActionSerializer(many=True, source='todo_action')

    def get_action_count(self, obj: TODOList):
        return obj.todo_action.count()

    class Meta:
        model = TODOList
        fields = ['id', 'title', 'slug', 'created', 'updated', 'order', 'action_count', 'actions']

