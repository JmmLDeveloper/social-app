
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Token, User, Post
from .factories import UserFactory,PostFactory


class UserRegistrationTestCase(APITestCase):
    url = reverse('main:register')

    def test_valid_registration(self):
        registration_data = {
            'username': "mr_new_user",
            'first_name': "newton usurum",
            'age': 25,
            'password1': "sec_PAS_1*2",
            'password2': "sec_PAS_1*2",
            'description': 'i am a new user that is being tested'
        }
        response = self.client.post(self.url, registration_data)
        # test that request was successfully
        self.assertEqual(201, response.status_code)
        user_id = response.json().get('user').get('id')
        token = response.json().get('token')
        # test that user was created
        user = User.objects.get(id=user_id)
        # test that the token was attached to the user
        token = Token.objects.get(value=token, user=user)

    def test_weak_password_registration(self):
        registration_data = {
            'username': "mr_new_user",
            'first_name': "newton usurum",
            'age': 25,
            'password1': "123",
            'password2': "123",
            'description': 'i am a new user that is being tested'
        }
        response = self.client.post(self.url, registration_data)
        self.assertEqual(400, response.status_code)
        password1 = response.json().get('password1')
        # there is problem with the password
        self.assertTrue(password1)

class PostUsageTestCase(APITestCase):

    def setUp(self):
        self.userA = UserFactory.create(username='UserA')
        self.userB = UserFactory.create(username='UserB')



        self.tokenA = Token.create(self.userA)
        self.tokenB = Token.create(self.userB)

        self.PostByA = PostFactory.create(author=self.userA)

        self.url = reverse('main:post-detail', kwargs={'pk': self.PostByA.id})

    def test_forbbiden_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokenB.value)
        response = client.delete(self.url)
        # should return forbbiden
        self.assertEqual(response.status_code, 403)

    def test_valid_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.tokenA.value)
        response = client.delete(self.url)
        # should allow deletion and return 204
        self.assertEqual(response.status_code, 204)
