from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError("O e-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("accepted_terms", True)
        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError("Superusuário precisa ser staff e superusuário.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Conta do responsável; crianças nunca possuem conta de autenticação."""
    username = None
    email = models.EmailField("e-mail", unique=True)
    full_name = models.CharField("nome do responsável", max_length=150)
    accepted_terms = models.BooleanField("aceitou termos", default=False)
    consented_at = models.DateTimeField("data do consentimento", null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    def __str__(self) -> str:
        return self.email


class ChildProfile(models.Model):
    """Dados mínimos da criança; sempre pertencem a um único responsável."""
    AVATARS = [("star", "Estrela"), ("rocket", "Foguete"), ("leaf", "Folha"), ("cloud", "Nuvem")]
    guardian = models.ForeignKey(User, on_delete=models.CASCADE, related_name="children")
    nickname = models.CharField(max_length=40)
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    school_year = models.ForeignKey("curriculum.SchoolYear", on_delete=models.PROTECT)
    avatar = models.CharField(max_length=16, choices=AVATARS, default="star")
    favorite_color = models.CharField(max_length=16, default="#5B5BD6")
    total_xp = models.PositiveIntegerField(default=0)
    coins = models.PositiveIntegerField(default=0)
    hearts = models.PositiveSmallIntegerField(default=5)
    last_activity_date = models.DateField(null=True, blank=True)
    audio_enabled = models.BooleanField(default=True)
    class Meta: ordering = ("nickname",)
    def __str__(self): return self.nickname
