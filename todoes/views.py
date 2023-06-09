from .serializers import TodoSerializer, TodoCreateSerializer
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Todo


class TodoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        todo = Todo.objects.filter(user_id=request.user)
        serializer = TodoSerializer(todo, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TodoCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 모든 할 일 삭제
    def delete(self, request):
        todo = Todo.objects.filter(user_id=request.user)
        total = todo.count()
        todo.delete()
        return Response(f"모든 항목({total}개)를 삭제했습니다!", status=status.HTTP_404_NOT_FOUND)


class TodoDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, request, todo_id):
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        return todo

    def get(self, request, todo_id):
        todo = self.get_object(request, todo_id)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, todo_id):
        todo = self.get_object(request, todo_id)
        serializer = TodoSerializer(todo, data=request.data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, todo_id):
        self.get_object(request, todo_id).delete()
        return Response("삭제 되었습니다!", status=status.HTTP_204_NO_CONTENT)
