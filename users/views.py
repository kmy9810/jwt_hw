from .serializers import UserSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User


class UserView(APIView):
    def get_object(self, request):
        user = get_object_or_404(User, email=request.user)
        return user

    def get(self, request):
        user = self.get_object(request)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = self.get_object(request)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = self.get_object(request)
        user.delete()
        return Response("존재 하지 않는 유저 입니다.", status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


