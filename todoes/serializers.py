from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from .models import Todo
from rest_framework.serializers import ValidationError
from datetime import datetime, date


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def validate(self, attrs):
        if len(attrs['title']) < 5:
            raise ValidationError("5자 이상 부터 등록이 가능합니다!")
        return attrs

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
        fields = ['id', 'title', 'is_complete', 'do_at', 'created_at']


class TodoCreateSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        if len(attrs['title']) < 5:
            raise ValidationError("5자 이상 부터 등록이 가능합니다!")
        existing_todo = Todo.objects.filter(
            do_at=attrs['do_at'],
            title=attrs['title'],
            user_id=user_id
        ).exists()
        if existing_todo:
            raise ValidationError("이미 존재 하는 할 일 입니다!")
        # 과거의 할 일을 등록 하면 안될까?
        # if attrs['do_at'] < date.today():
        #     raise ValidationError(f"'{date.today()}'보다 과거는 불가합니다.")
        return attrs

    class Meta:
        model = Todo
        fields = ['title', 'do_at']



