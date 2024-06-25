from django.test import TestCase
from django.forms import ValidationError
from api.models.user import User, UserManager


class TestUserManager(TestCase):

    """Tests for Base User Manager"""

    def test_create_user_with_email(self):
        
        """Tests user creation with email"""
        
        user = User.objects.create_user(
            email='test@mail.com',
            first_name='Test',
            last_name='User',
            password='testuserpassword123'
        )
        self.assertEqual(user.email, 'test@mail.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.check_password('testuserpassword123'))
    
    def test_create_user_without_email(self):

        """Tests user creation without email raises ValidationError"""

        with self.assertRaises(ValidationError):
            User.objects.create_user(
                email='',
                first_name='Test',
                last_name='User',
                password='testuserpassword123'
            )
    
    def test_create_superuser(self):
        
        """Tests superuser creation"""

        superuser = User.objects.create_superuser(
            email='admin@mail.com',
            first_name='Test',
            last_name='Admin',
            password='testadminpassword123'
        )
        self.assertEqual(superuser.email, 'admin@mail.com')
        self.assertEqual(superuser.first_name, 'Test')
        self.assertEqual(superuser.last_name, 'Admin')
        self.assertTrue(superuser.check_password('testadminpassword123'))
        self.assertTrue(superuser.is_verified)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)


class TestUserModel(TestCase):

    """Tests for Base User Model"""

    def test_user_fields(self):
        
        """Tests user fields after user creation"""

        user = User.objects.create_user(
            email = 'test@mail.com',
            first_name='Test',
            last_name='User',
            password='testuserpassword123'
        )
        self.assertEqual(user.email, 'test@mail.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
        self.assertFalse(user.is_staff)
    
    def test_string_representation(self):
        
        """Tests string representation of users"""

        user = User.objects.create_user(
            email='test@mail.com',
            first_name='Test',
            last_name='User',
            password='testuserpassword123'
        )
        self.assertEqual(str(user), 'test@mail.com')