from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User
from .models import Todo
from .serializers import TodoSerializer
from faker import Faker


# python manage.py test todoes
class TodoCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {'email': 'miyeong@naver.com', 'password': '1234'}
        cls.user = User.objects.create_user(username='mimi', email='miyeong@naver.com', password='1234')
        cls.todo_data = {'title': 'some title', 'do_at':'2023-02-23'}
        cls.faker = Faker()
        cls.todos = []
        for i in range(10):
            cls.todos.append(Todo.objects.create(title=cls.faker.sentence(), user=cls.user,
                                                 do_at=cls.faker.date()))

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']

    # 로그인 안했을 시
    def test_fail_if_not_logged_in(self):
        url = reverse('todo_view')
        response = self.client.post(url, self.todo_data)
        self.assertEquals(response.status_code, 401)

    # 할 일 리스트 확인 테스트
    def test_get_todo_list(self):
        response = self.client.get(
            path=reverse('todo_view'),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEquals(response.status_code, 200)

    # 할 일 작성 테스트
    def test_create_todo(self):
        response = self.client.post(
            path=reverse('todo_view'),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.todo_data
        )
        self.assertEquals(response.status_code, 201)

    def test_all_delete_todo(self):
        response = self.client.delete(
            path=reverse('todo_view'),
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
            data=self.todo_data
        )
        self.assertEquals(response.status_code, 404)


class TodoDetailTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.data = {'email': 'miyeong@naver.com', 'password': '1234'}
        cls.user = User.objects.create_user(username='mimi', email='miyeong@naver.com', password='1234')
        cls.todos = []
        for i in range(10):
            cls.todos.append(Todo.objects.create(title=cls.faker.sentence(), user=cls.user,
                                                 do_at=cls.faker.date()))

    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']

    # 할 일 디테일 보기 테스트
    def test_get_todo(self):
        for todo in self.todos:
            url = todo.get_absolute_url()
            response = self.client.get(path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
            serializer = TodoSerializer(todo).data
            for k, v in serializer.items():
                self.assertEquals(response.data[k], v)

    # 할 일 수정 테스트
    def test_patch_todo(self):
        for todo in self.todos:
            url = todo.get_absolute_url()
            response = self.client.patch(path=url,
                                         HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
                                         data={'title': self.faker.sentence()})
            print(response.data)
            self.assertEquals(response.status_code, 200)

    # 할 일 삭제 테스트
    def test_delete_todo(self):
        for todo in self.todos:
            url = todo.get_absolute_url()
            response = self.client.delete(path=url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
            self.assertEquals(response.status_code, 204)


