from datetime import timedelta
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from accounts.models import ChildProfile, User
from curriculum.models import Exercise, SchoolYear
from .models import LessonProgress

class LearningFlowTests(TestCase):
    def setUp(self):
        call_command("seed_initial_curriculum")
        self.user = User.objects.create_user("guardian@example.com", "SenhaForte123!", full_name="Responsável", accepted_terms=True)
        self.other = User.objects.create_user("other@example.com", "SenhaForte123!", full_name="Outro", accepted_terms=True)
        year = SchoolYear.objects.get(order=1)
        self.child = ChildProfile.objects.create(guardian=self.user, nickname="Nina", school_year=year)
        self.other_child = ChildProfile.objects.create(guardian=self.other, nickname="Léo", school_year=year)
        self.client.force_login(self.user)
        session = self.client.session; session["active_child_id"] = self.child.pk; session.save()

    def test_other_guardian_cannot_select_profile(self):
        self.assertEqual(self.client.get(reverse("choose_profile", args=[self.other_child.pk])).status_code, 404)

    def test_correct_answer_completes_and_unlocks_next(self):
        exercise = Exercise.objects.get(lesson__order=1)
        response = self.client.post(reverse("answer", args=[exercise.pk]), {"answer": exercise.correct_answer})
        self.assertContains(response, "Muito bem")
        self.child.refresh_from_db()
        self.assertGreater(self.child.total_xp, 0)
        self.assertTrue(LessonProgress.objects.filter(child=self.child, lesson=exercise.lesson, state=LessonProgress.COMPLETED).exists())
        self.assertTrue(LessonProgress.objects.filter(child=self.child, lesson__order=2, state=LessonProgress.AVAILABLE).exists())
        self.assertEqual(self.child.masteries.get(skill=exercise.lesson.primary_skill).review_due_at, timezone.localdate() + timedelta(days=1))

    def test_path_marks_future_lessons_as_locked(self):
        response = self.client.get(reverse("learning_path"))
        self.assertContains(response, "Complete a anterior")
        self.assertNotContains(response, reverse("lesson", args=[Exercise.objects.get(lesson__order=3).lesson.pk]))
