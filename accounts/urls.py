from django.urls import path
from . import views

urlpatterns = [path("criar/", views.signup, name="signup"), path("perfis/", views.profiles, name="profiles"), path("perfis/novo/", views.create_profile, name="create_profile"), path("perfis/<int:pk>/usar/", views.choose_profile, name="choose_profile"), path("perfis/<int:pk>/editar/", views.edit_profile, name="edit_profile"), path("perfis/<int:pk>/excluir/", views.delete_profile, name="delete_profile")]
