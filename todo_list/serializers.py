from rest_framework import serializers
from .models import Todo
from users.models import User
from datetime import datetime


class TodoSerializer(serializers.ModelSerializer):
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Todo
        fields = '__all__'

    def update(self, instance, validated_data):
        # patch를 사용 하기 위에 값이 들어 오지 않으면 원래 상태, 아니면 수정된 데이터 저장
        instance.title = validated_data.get('title', instance.title)
        instance.is_complete = validated_data.get('is_complete', instance.is_complete)
        if validated_data.get('is_complete'):  # todo 완료시 시간
            instance.completion_at = datetime.now()
        if validated_data.get('title'):  # todo title 변경시 시간
            instance.updated_at = datetime.now()
        instance.save()
        return instance


class TodoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title', 'is_complete', 'created_at']


class TodoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['title',]

