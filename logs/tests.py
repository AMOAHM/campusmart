from django.test import TestCase
from .models import SystemLog
from accounts.models import User


class SystemLogTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='admin'
        )
    
    def test_system_log_creation(self):
        log = SystemLog.objects.create(
            user=self.user,
            action='login',
            description='User logged in',
            ip_address='127.0.0.1'
        )
        self.assertEqual(log.user.username, 'testuser')
        self.assertEqual(log.action, 'login')
