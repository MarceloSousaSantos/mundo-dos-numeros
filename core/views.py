from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from learning.models import LessonProgress

def home(request):
    return render(request, "core/home.html")

def health(request):
    return JsonResponse({"status": "ok"})

@login_required
def guardian_dashboard(request):
    cards = []
    for child in request.user.children.all():
        masteries = child.masteries.select_related("skill").order_by("-score")
        cards.append({"child": child, "completed": child.lesson_progress.filter(state=LessonProgress.COMPLETED).count(), "attempts": child.attempts.count(), "strong": masteries.filter(score__gte=80)[:3], "review": masteries.filter(review_due_at__lte=timezone.localdate())[:3], "recent": child.attempts.select_related("exercise__lesson").order_by("-created_at")[:5]})
    return render(request, "core/dashboard.html", {"cards": cards})

@login_required
def privacy(request):
    if request.method == "POST":
        if request.user.check_password(request.POST.get("password", "")):
            user = request.user; logout(request); user.delete()
            messages.success(request, "Sua conta e os dados vinculados foram excluídos.")
            return redirect("home")
        messages.error(request, "A senha informada não confere.")
    return render(request, "core/privacy.html")
