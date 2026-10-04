from django.test import TestCase
from django.urls import reverse
from accounts.models import User

class GuardianPanelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("parent@example.com", "SenhaForte123!", full_name="Pat")
        self.client.force_login(self.user)

    def test_dashboard_is_private(self):
        self.assertEqual(self.client.get(reverse("guardian_dashboard")).status_code, 200)

    def test_account_deletion_requires_correct_password(self):
        response = self.client.post(reverse("privacy"), {"password": "errada"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())
