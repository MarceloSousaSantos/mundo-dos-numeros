from django.db import models

class Attempt(models.Model):
    child = models.ForeignKey("accounts.ChildProfile", on_delete=models.CASCADE, related_name="attempts")
    exercise = models.ForeignKey("curriculum.Exercise", on_delete=models.CASCADE)
    submitted_answer = models.JSONField()
    is_correct = models.BooleanField()
    attempt_number = models.PositiveSmallIntegerField(default=1)
    used_hint = models.BooleanField(default=False)
    response_time_seconds = models.PositiveIntegerField(default=0)
    origin = models.CharField(max_length=10, default="click")
    created_at = models.DateTimeField(auto_now_add=True)

class LessonProgress(models.Model):
    LOCKED, AVAILABLE, STARTED, COMPLETED = "locked", "available", "started", "completed"
    STATES = [(LOCKED, "Bloqueada"), (AVAILABLE, "Disponível"), (STARTED, "Iniciada"), (COMPLETED, "Concluída")]
    child = models.ForeignKey("accounts.ChildProfile", on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey("curriculum.Lesson", on_delete=models.CASCADE)
    state = models.CharField(max_length=12, choices=STATES, default=LOCKED)
    best_score = models.PositiveSmallIntegerField(default=0)
    completion_count = models.PositiveIntegerField(default=0)
    last_completed_at = models.DateTimeField(null=True, blank=True)
    class Meta: constraints = [models.UniqueConstraint(fields=("child", "lesson"), name="one_progress_per_child_lesson")]

class SkillMastery(models.Model):
    child = models.ForeignKey("accounts.ChildProfile", on_delete=models.CASCADE, related_name="masteries")
    skill = models.ForeignKey("curriculum.Skill", on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(default=0)
    last_practiced_at = models.DateTimeField(null=True, blank=True)
    review_due_at = models.DateField(null=True, blank=True)
    class Meta: constraints = [models.UniqueConstraint(fields=("child", "skill"), name="one_mastery_per_child_skill")]
