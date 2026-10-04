from django.contrib import admin
from .models import Exercise, LearningPath, Lesson, SchoolYear, Skill

class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 0
    fields = ("order", "exercise_type", "prompt", "is_active")

@admin.register(SchoolYear)
class SchoolYearAdmin(admin.ModelAdmin): list_display = ("name", "recommended_age", "order", "is_active"); list_editable = ("order", "is_active")
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin): list_display = ("bncc_code", "title", "school_year", "order"); list_filter = ("school_year",); search_fields = ("bncc_code", "title")
@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin): list_display = ("name", "school_year", "order", "color"); list_filter = ("school_year",)
@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "path", "primary_skill", "order", "is_active"); list_filter = ("path", "is_active"); search_fields = ("title",); inlines = (ExerciseInline,)
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin): list_display = ("lesson", "order", "exercise_type", "difficulty", "is_active"); list_filter = ("exercise_type", "is_active"); search_fields = ("prompt",)
