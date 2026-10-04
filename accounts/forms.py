from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import User


class GuardianSignupForm(UserCreationForm):
    accepted_terms = forms.BooleanField(label="Li e aceito os termos e a política de privacidade")

    class Meta:
        model = User
        fields = ("full_name", "email", "accepted_terms", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.consented_at = timezone.now()
        if commit:
            user.save()
        return user
