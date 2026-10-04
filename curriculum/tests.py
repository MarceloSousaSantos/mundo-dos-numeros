from django.core.management import call_command
from django.test import TestCase
from .models import Exercise, Lesson, SchoolYear

class SeedTests(TestCase):
    def test_seed_is_idempotent_and_creates_twenty_lessons(self):
        call_command("seed_initial_curriculum")
        call_command("seed_initial_curriculum")
        self.assertEqual(Lesson.objects.count(), 20)
        self.assertEqual(Exercise.objects.count(), 20)
        self.assertEqual(SchoolYear.objects.count(), 3)
