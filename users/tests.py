from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user_data = {
            "first_name": "Sarvarbek",
            "last_name": "Juraev",
            "email": "test@example.com",
            "password": "securepassword123",
        }

    def test_create_user_successfully(self):
        user = User.objects.create_user(**self.user_data)

        self.assertEqual(user.first_name, "Sarvarbek")
        self.assertEqual(user.last_name, "Juraev")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepassword123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_verified)  # default in create_user
        self.assertTrue(user.is_active)

    def test_create_user_missing_email(self):
        data = self.user_data.copy()
        data["email"] = ""
        with self.assertRaises(ValueError):
            User.objects.create_user(**data)

    def test_create_superuser_successfully(self):
        admin_user = User.objects.create_superuser(**self.user_data)

        self.assertEqual(admin_user.email, "test@example.com")
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_verified)
        self.assertTrue(admin_user.is_active)

    def test_email_is_unique(self):
        User.objects.create_user(**self.user_data)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.user_data)

    def test_email_is_normalized(self):
        mixed_case_email = "Test@Example.COM"
        user = User.objects.create_user(
            first_name="Test",
            last_name="User",
            email=mixed_case_email,
            password="12345test",
        )
        self.assertEqual(user.email, "test@example.com")

    def test_required_fields(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="user@example.com")

    def test_str_representation(self):
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), user.email)  # if you define `__str__` method later
