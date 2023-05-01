from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from todoes.serializers import TodoDetailSerializer
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.core.exceptions import ValidationError
from .validators import (contains_special_character, check_password)
from todoes.models import Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # patch를 사용 하기 위에 값이 들어 오지 않으면 원래 상태, 아니면 수정된 데이터 저장
        if validated_data.get('email'):
            raise ValidationError("이메일은 변경할 수 없습니다!")
        if validated_data.get('username'):
            if contains_special_character(validated_data['username']):
                raise ValidationError("이름에 특수문자와 초성을 사용할 수 없습니다!")
        if validated_data.get('password'):
            if check_password(validated_data['password']):
                raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다!")
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    todo_set = TodoDetailSerializer(many=True, read_only=True)
    success_todo_count = serializers.SerializerMethodField()
    all_todo_count = serializers.SerializerMethodField()

    def get_success_todo_count(self, obj):
        success = Todo.objects.filter(is_complete=True, user_id=obj.id).count()
        return f'{success}개'

    def get_all_todo_count(self, obj):
        all = Todo.objects.filter(user_id=obj.id).count()
        return f'{all}개'

    class Meta:
        model = User
        fields = ['username', 'email', 'gender', 'age', 'introduction', 'all_todo_count',
                  'success_todo_count', 'todo_set']
        extra_kwargs = {
            'todo_set': {'read_only': True},
        }


# jwt 토큰 커스텀
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['gender'] = user.gender
        token['age'] = user.age
        return token
