from django.test import TestCase
from django.urls import reverse
from .models import User

class AccountTests(TestCase):
    def test_guardian_can_sign_up_with_email(self):
        response = self.client.post(reverse("signup"), {"full_name": "Ana Silva", "email": "ana@example.com", "accepted_terms": "on", "password1": "Seguro12345!", "password2": "Seguro12345!"})
        self.assertRedirects(response, reverse("home"))
        user = User.objects.get(email="ana@example.com")
        self.assertTrue(user.check_password("Seguro12345!"))
        self.assertIsNotNone(user.consented_at)

    def test_home_and_health_are_public(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertJSONEqual(self.client.get(reverse("health")).content, {"status": "ok"})

    def test_guardian_cannot_delete_another_profile(self):
        from curriculum.models import SchoolYear
        from .models import ChildProfile
        first, _ = SchoolYear.objects.get_or_create(name="Teste", defaults={"recommended_age": "6", "order": 99})
        owner = User.objects.create_user("owner@example.com", "SenhaForte123!", full_name="Dona")
        other = User.objects.create_user("other@example.com", "SenhaForte123!", full_name="Outro")
        child = ChildProfile.objects.create(guardian=owner, nickname="Lia", school_year=first)
        self.client.force_login(other)
        self.assertEqual(self.client.post(reverse("delete_profile", args=[child.pk])).status_code, 404)
