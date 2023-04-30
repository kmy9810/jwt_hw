from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User


class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {'email': 'miyeong1@naver.com', 'password': 'Aldud3015^^'}
        self.data2 = {'email': 'miyeong2@naver.com', 'password': 'Aldud3015^^', 'username':'안녕'}
        self.user = User.objects.create_user(username='miyeong1', email='miyeong1@naver.com', password='Aldud3015^^')

    # 유저 회원 가입 테스트
    def test_signup(self):
        response = self.client.post(reverse('user_view'), self.data2)
        print(response.data)

    # 유저 로그인 테스트
    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEquals(response.status_code, 200)

    # 유저 프로필 확인 테스트
    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.get(path=reverse('user_view'),
                                   HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEquals(response.data['email'], self.data['email'])

    # 유저 정보 변경 테스트
    def test_patch_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.patch(path=reverse('user_view'),
                                     HTTP_AUTHORIZATION=f"Bearer {access_token}",
                                     data={'age': 25, 'introduction': "수정했지롱", 'gender': "female"})
        self.assertEquals(response.data['email'], self.data['email'])

    # 유효성 검사 실패 테스트
    def test_patch_false_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.patch(path=reverse('user_view'),
                                     HTTP_AUTHORIZATION=f"Bearer {access_token}",
                                     data={'username':'@#$%^', 'password':'as234SD', 'email':'slhwe'})
        self.assertEquals(response.status_code, 400)

    # 유저 탈퇴 테스트
    def test_delete_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.delete(path=reverse('user_view'),
                                      HTTP_AUTHORIZATION=f"Bearer {access_token}", )
        self.assertEquals(response.status_code, 404)
