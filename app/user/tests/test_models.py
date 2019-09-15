from django.test import TestCase
from django.contrib.auth import get_user_model


def sample_user():
    '''helper to create a sample user'''
    email = 'tito@pluto.com'
    password = 'testpass'

    user = get_user_model().objects.create_user(
        email=email,
        password=password
    )
    return user


class UserModelTests(TestCase):
    """ Test class for the User Model"""

    def test_create_user_with_email_successful(self):
        """ Test creating a user with an email is successful"""
        email = 'tito@pluto.com'
        password = 'testpass'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'tito@PLUTO.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'tito@pluto.com',
            'testpass'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
