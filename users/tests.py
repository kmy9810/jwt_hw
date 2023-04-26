from django.urls import reverse
from rest_framework.test import APITestCase
from .models import User


class LoginUserTest(APITestCase):
    def setUp(self):
        self.data = {'email': 'miyeong@naver.com', 'password': 'Aldud3015^^'}
        # "email": "miyeong@naver.com", "gender": "female", "age": 26, "introduction": "hi"
        self.user = User.objects.create_user('miyeong@naver.com', 'Aldud3015^^')


    def test_signup(self):
        response = self.client.post(reverse('user_view'), self.data)
        print(response)

    def test_login(self):
        response = self.client.post(reverse('token_obtain_pair'), self.data)
        self.assertEquals(response.status_code, 200)

    # 유저 프로필 확인 테스트
    def test_get_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.get(path=reverse('profile_view'),
                                   HTTP_AUTHORIZATION=f"Bearer {access_token}")
        self.assertEquals(response.data['email'], self.data['email'])

    # 유저 정보 변경 테스트
    def test_patch_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.patch(path=reverse('profile_view'),
                                     HTTP_AUTHORIZATION=f"Bearer {access_token}",
                                     data={'age': 25, 'introduction': "수정했지롱", 'gender': "female"})
        self.assertEquals(response.data['email'], self.data['email'])
        # self.assertEquals(response.status_code, 400)

    # 유저 탈퇴 테스트
    def test_delete_user_data(self):
        access_token = self.client.post(reverse('token_obtain_pair'), self.data).data['access']
        response = self.client.delete(path=reverse('profile_view'),
                                      HTTP_AUTHORIZATION=f"Bearer {access_token}", )
        self.assertEquals(response.status_code, 404)
