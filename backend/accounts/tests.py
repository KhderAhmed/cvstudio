from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


class AuthenticationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "Strong-CV!84-Blue",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())
        user = User.objects.get(username="newuser")
        self.assertTrue(user.check_password("Strong-CV!84-Blue"))
        self.assertNotIn("password", response.data)

    def test_register_rejects_weak_password(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "weakuser",
                "email": "weakuser@example.com",
                "password": "short",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)
        self.assertFalse(User.objects.filter(username="weakuser").exists())

    def test_jwt_login_and_me_endpoint(self):
        user = User.objects.create_user(
            username="engineer",
            password="Strong-Test-Password!42",
            email="engineer@example.com",
        )

        anonymous = self.client.get(reverse("me"))
        self.assertEqual(anonymous.status_code, 401)

        token_response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": user.username, "password": "Strong-Test-Password!42"},
            format="json",
        )
        self.assertEqual(token_response.status_code, 200)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )
        me_response = self.client.get(reverse("me"))
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.data["username"], user.username)