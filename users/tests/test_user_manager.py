from django.test import TestCase
import pytest
from users.models import CustomUser

@pytest.mark.django_db()
class TestUserSchema(TestCase):
    CORRECT_EMAIL = "test@test.com"
    CORRECT_PASSWORD = "q&YsAp-Y8)KYd.H^"
    CORRECT_USERNAME = "test"
    def test_manager_create_user(self):
        CustomUser.objects._create_user(
            email=self.CORRECT_EMAIL, username = self.CORRECT_USERNAME, password=self.CORRECT_PASSWORD
        )
        user = CustomUser.objects.filter(email=self.CORRECT_EMAIL)
        assert int(user.count()) == 1