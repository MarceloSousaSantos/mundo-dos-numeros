from django.urls import path
from . import views
urlpatterns = [path("trilha/", views.learning_path, name="learning_path"), path("licao/<int:pk>/", views.lesson, name="lesson"), path("exercicio/<int:pk>/responder/", views.answer, name="answer")]
