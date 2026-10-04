from django.db import models


class SchoolYear(models.Model):
    name = models.CharField(max_length=80, unique=True)
    recommended_age = models.CharField(max_length=30)
    order = models.PositiveSmallIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ("order",)
    def __str__(self): return self.name


class Skill(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name="skills")
    bncc_code = models.CharField(max_length=30)
    title = models.CharField(max_length=160)
    description = models.TextField()
    thematic_unit = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=1)
    class Meta:
        ordering = ("school_year__order", "order")
        constraints = [models.UniqueConstraint(fields=("school_year", "bncc_code"), name="unique_skill_per_year")]
    def __str__(self): return f"{self.bncc_code} — {self.title}"


class LearningPath(models.Model):
    school_year = models.ForeignKey(SchoolYear, on_delete=models.PROTECT, related_name="paths")
    name = models.CharField(max_length=120)
    description = models.TextField()
    color = models.CharField(max_length=20, default="#5B5BD6")
    icon = models.CharField(max_length=30, default="✦")
    order = models.PositiveSmallIntegerField(default=1)
    class Meta:
        ordering = ("school_year__order", "order")
        constraints = [models.UniqueConstraint(fields=("school_year", "name"), name="unique_path_per_year")]
    def __str__(self): return self.name


class Lesson(models.Model):
    path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, related_name="lessons")
    primary_skill = models.ForeignKey(Skill, on_delete=models.PROTECT, related_name="lessons")
    title = models.CharField(max_length=160)
    description = models.TextField()
    order = models.PositiveSmallIntegerField()
    xp_reward = models.PositiveSmallIntegerField(default=10)
    recommended_exercise_count = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=True)
    prerequisite = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="unlocks")
    class Meta:
        ordering = ("path__order", "order")
        constraints = [models.UniqueConstraint(fields=("path", "order"), name="unique_lesson_order_per_path")]
    def __str__(self): return self.title


class Exercise(models.Model):
    class Type(models.TextChoices):
        MULTIPLE_CHOICE = "choice", "Múltipla escolha"
        COUNTING = "count", "Contagem"
        COMPARISON = "compare", "Maior, menor ou igual"
        SEQUENCE = "sequence", "Completar sequência"
        INPUT = "input", "Digitar resultado"
        OPERATION = "operation", "Montar operação"
        DRAG_DROP = "drag", "Arrastar e soltar"
        NUMBER_LINE = "line", "Reta numérica"
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="exercises")
    exercise_type = models.CharField(max_length=12, choices=Type.choices)
    prompt = models.TextField()
    short_instruction = models.CharField(max_length=180)
    data = models.JSONField(default=dict, blank=True)
    correct_answer = models.JSONField()
    explanation = models.TextField()
    hint = models.TextField()
    difficulty = models.PositiveSmallIntegerField(default=1)
    order = models.PositiveSmallIntegerField(default=1)
    audio_path = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        ordering = ("lesson__order", "order")
        constraints = [models.UniqueConstraint(fields=("lesson", "order"), name="unique_exercise_order_per_lesson")]
    def __str__(self): return f"{self.lesson}: exercício {self.order}"
