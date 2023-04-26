from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from todo_list.serializers import TodoDetailSerializer
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from .validators import (contains_special_character, check_password, check_email)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(validators=[UniqueValidator(
        queryset=User.objects.all(),  # 필수 옵션!
        message='이미 존재하는 이메일입니다.',  # 필수 아님!
    )])

    def validate(self, attrs):
        if attrs.get('email'):
            if check_email(attrs['email']):
                raise ValidationError("이메일에는 '@'와 '.'이 반드시 포함 되어야 합니다!")
        if attrs.get('name'):
            if contains_special_character(attrs['name']):
                raise ValidationError("이름에 특수문자를 사용할 수 없습니다!")
        if attrs.get('password'):
            if check_password(attrs['password']):
                raise ValidationError("8자 이상의 영문 대/소문자, 숫자, 특수문자 조합이어야 합니다!")
        return attrs

    class Meta:
        model = User
        fields = '__all__'

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

        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    todo_set = TodoDetailSerializer(many=True, read_only=True)
    email = serializers.CharField(validators=[UniqueValidator(
        queryset=User.objects.all(),  # 필수 옵션!
        message='이미 존재하는 이메일입니다.',  # 필수 아님!
    )])

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'gender', 'introduction', 'age', 'todo_set']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['name'] = user.name
        token['gender'] = user.gender
        token['age'] = user.age
        return token
