from datetime import timedelta
from django.utils import timezone
from .models import Achievement, AchievementUnlock, DailyStreak

def register_daily_activity(child):
    today = timezone.localdate()
    streak, _ = DailyStreak.objects.get_or_create(child=child)
    if streak.last_activity_date == today: return streak
    streak.count = streak.count + 1 if streak.last_activity_date == today - timedelta(days=1) else 1
    streak.last_activity_date = today; streak.save()
    if streak.count >= 3:
        badge, _ = Achievement.objects.get_or_create(name="Três dias de descoberta", defaults={"description": "Aprendeu em três dias diferentes.", "icon": "☀", "criterion": "streak_3"})
        AchievementUnlock.objects.get_or_create(achievement=badge, child=child)
    return streak
