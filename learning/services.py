from datetime import timedelta
from django.db import transaction
from django.utils import timezone
from .models import Attempt, LessonProgress, SkillMastery
from gamification.services import register_daily_activity

def same_answer(answer, correct): return str(answer).strip().lower() == str(correct).strip().lower()

REVIEW_INTERVALS = (1, 3, 7, 14)

@transaction.atomic
def record_answer(child, exercise, answer, used_hint=False):
    previous = Attempt.objects.filter(child=child, exercise=exercise).count()
    correct = same_answer(answer, exercise.correct_answer)
    attempt = Attempt.objects.create(child=child, exercise=exercise, submitted_answer=answer, is_correct=correct, attempt_number=previous + 1, used_hint=used_hint)
    mastery, _ = SkillMastery.objects.get_or_create(child=child, skill=exercise.lesson.primary_skill)
    if correct:
        mastery.score = min(100, mastery.score + (12 if previous == 0 and not used_hint else 5))
        mastery.last_practiced_at = timezone.now()
        successful_practices = Attempt.objects.filter(child=child, exercise__lesson__primary_skill=mastery.skill, is_correct=True).count()
        interval = REVIEW_INTERVALS[min(successful_practices - 1, len(REVIEW_INTERVALS) - 1)]
        mastery.review_due_at = timezone.localdate() + timedelta(days=interval)
        child.total_xp += exercise.lesson.xp_reward if previous == 0 else 2; child.coins += 2 if previous == 0 else 0
    else:
        mastery.score = max(0, mastery.score - 2); child.hearts = max(0, child.hearts - 1)
    mastery.save(); child.last_activity_date = timezone.localdate(); child.save(); register_daily_activity(child)
    return attempt, mastery

@transaction.atomic
def complete_lesson(child, lesson):
    progress, _ = LessonProgress.objects.get_or_create(child=child, lesson=lesson)
    progress.state = LessonProgress.COMPLETED; progress.best_score = 100; progress.completion_count += 1; progress.last_completed_at = timezone.now(); progress.save()
    next_lesson = lesson.path.lessons.filter(order=lesson.order + 1, is_active=True).first()
    if next_lesson: LessonProgress.objects.get_or_create(child=child, lesson=next_lesson, defaults={"state": LessonProgress.AVAILABLE})
