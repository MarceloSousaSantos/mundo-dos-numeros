from django.urls import path
from . import views
urlpatterns = [path("", views.home, name="home"), path("health/", views.health, name="health"), path("responsavel/", views.guardian_dashboard, name="guardian_dashboard"), path("privacidade/", views.privacy, name="privacy")]
