from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import ChildProfile
from curriculum.models import Exercise, LearningPath, Lesson
from .models import LessonProgress
from .services import complete_lesson, record_answer

def current_child(request):
    child_id = request.session.get("active_child_id")
    if not child_id: return None
    return get_object_or_404(ChildProfile, pk=child_id, guardian=request.user)

@login_required
def learning_path(request):
    child = current_child(request)
    if not child: return redirect("profiles")
    path = LearningPath.objects.filter(school_year=child.school_year).first()
    lessons = list(path.lessons.filter(is_active=True)) if path else []
    progress = {p.lesson_id: p.state for p in LessonProgress.objects.filter(child=child, lesson__in=lessons)}
    lesson_cards = []
    for item in lessons:
        state = progress.get(item.pk)
        available = not item.prerequisite or progress.get(item.prerequisite_id) == LessonProgress.COMPLETED
        if state is None:
            state = LessonProgress.AVAILABLE if available else LessonProgress.LOCKED
        lesson_cards.append({"lesson": item, "state": state, "available": available})
    return render(request, "learning/path.html", {"child": child, "path": path, "lesson_cards": lesson_cards, "streak": getattr(child, "streak", None)})

@login_required
def lesson(request, pk):
    child = current_child(request)
    if not child: return redirect("profiles")
    lesson = get_object_or_404(Lesson, pk=pk, path__school_year=child.school_year, is_active=True)
    if lesson.prerequisite and not LessonProgress.objects.filter(child=child, lesson=lesson.prerequisite, state=LessonProgress.COMPLETED).exists(): return redirect("learning_path")
    LessonProgress.objects.get_or_create(child=child, lesson=lesson, defaults={"state": LessonProgress.STARTED})
    return render(request, "learning/lesson.html", {"child": child, "lesson": lesson, "exercise": lesson.exercises.filter(is_active=True).first()})

@login_required
def answer(request, pk):
    if request.method != "POST": return HttpResponseBadRequest("Use o formulário para responder.")
    child = current_child(request)
    if not child: return redirect("profiles")
    exercise = get_object_or_404(Exercise, pk=pk, lesson__path__school_year=child.school_year, is_active=True)
    attempt, mastery = record_answer(child, exercise, request.POST.get("answer", ""), request.POST.get("used_hint") == "1")
    if attempt.is_correct:
        complete_lesson(child, exercise.lesson)
        return render(request, "learning/result.html", {"child": child, "lesson": exercise.lesson, "mastery": mastery})
    return render(request, "learning/lesson.html", {"child": child, "lesson": exercise.lesson, "exercise": exercise, "feedback": "Quase! Veja a dica e tente outra vez.", "show_hint": True})
