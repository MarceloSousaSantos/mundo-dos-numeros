from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GuardianSignupForm
from .models import ChildProfile
from .profile_forms import ChildProfileForm


def signup(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = GuardianSignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "accounts/signup.html", {"form": form})

@login_required
def profiles(request):
    return render(request, "accounts/profiles.html", {"children": request.user.children.select_related("school_year")})

@login_required
def create_profile(request):
    form = ChildProfileForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        child = form.save(commit=False); child.guardian = request.user; child.save()
        request.session["active_child_id"] = child.pk
        return redirect("learning_path")
    return render(request, "accounts/profile_form.html", {"form": form})

@login_required
def choose_profile(request, pk):
    child = get_object_or_404(ChildProfile, pk=pk, guardian=request.user)
    request.session["active_child_id"] = child.pk
    return redirect("learning_path")

@login_required
def edit_profile(request, pk):
    child = get_object_or_404(ChildProfile, pk=pk, guardian=request.user)
    form = ChildProfileForm(request.POST or None, instance=child)
    if request.method == "POST" and form.is_valid():
        form.save(); return redirect("profiles")
    return render(request, "accounts/profile_form.html", {"form": form, "editing": child})

@login_required
def delete_profile(request, pk):
    child = get_object_or_404(ChildProfile, pk=pk, guardian=request.user)
    if request.method == "POST":
        if request.session.get("active_child_id") == child.pk: request.session.pop("active_child_id", None)
        child.delete(); return redirect("profiles")
    return render(request, "accounts/profile_delete.html", {"child": child})
