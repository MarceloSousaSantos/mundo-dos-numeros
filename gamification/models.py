from django.db import models

class Achievement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=30, default="✦")
    criterion = models.CharField(max_length=100)
    unlocked_by = models.ManyToManyField("accounts.ChildProfile", through="AchievementUnlock", blank=True)
    def __str__(self): return self.name

class AchievementUnlock(models.Model):
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    child = models.ForeignKey("accounts.ChildProfile", on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    class Meta: constraints = [models.UniqueConstraint(fields=("achievement", "child"), name="unique_achievement_unlock")]

class DailyStreak(models.Model):
    child = models.OneToOneField("accounts.ChildProfile", on_delete=models.CASCADE, related_name="streak")
    count = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
