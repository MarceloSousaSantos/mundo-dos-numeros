from django import forms
from .models import ChildProfile

class ChildProfileForm(forms.ModelForm):
    class Meta:
        model = ChildProfile
        fields = ("nickname", "birth_year", "school_year", "avatar", "favorite_color", "audio_enabled")
        widgets = {"favorite_color": forms.TextInput(attrs={"type": "color"})}
