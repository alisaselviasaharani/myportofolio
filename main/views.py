import os
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Education, Achievements
from main.forms import AchievementsForm


# VIEW PAGE HOME
def show_home(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "perkenalan": "Hello, I'm Alisa",
        "bio": "I'm a Computer Science student at Universitas Indonesia.",
        "bio1": "Welcome to my portofolio!!!",
        "bio2": "This is a little space where I share more about myself.",
    }

    return render(request, "home.html", context)


# VIEW PAGE ABOUTME
def show_aboutme(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "npm": "2506618433",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Computer Science student at Universitas Indonesia who is interested "
            "in learning, exploring new things, and developing skills in technology and data."
        ),
    }

    return render(request, "aboutme.html", context)


# VIEW PAGE EDUCATION
def show_education(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "education_list": Education.objects.all(),
    }

    return render(request, "education.html", context)


# VIEW PAGE EXPERIENCE
def show_experience(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)


# VIEW PAGE CREATE ACHIEVEMENTS
def create_achievements(request):
    form = AchievementsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["secret_code"] != os.getenv("PORTOFOLIO_SECRET"):
            form.add_error("secret_code", "TETOTT WKKWKWK Kode rahasia yang anda masukkan salah")
        else:
            form.save()
            messages.success(
                request,
                "Penghargaan baru berhasil ditambahkan!"
            )
            return redirect("main:show_achievements")

    context = {
        "name": "Alisa Selvia Saharani",
        "form": form,
    }

    return render(request, "achievements_form.html", context)


# VIEW PAGE ACHIEVEMENTS
def show_achievements(request):
    title_query = request.GET.get("title", "").strip()

    achievements = Achievements.objects.all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    # Serialize data menjadi JSON
    achievements_json = serializers.serialize("json", achievements)

    # Deserialize JSON kembali menjadi objek Django
    achievements_data = list(
        serializers.deserialize("json", achievements_json)
    )
    context = {
        "name": "Alisa Selvia Saharani",
        "achievements_list": achievements_data,
        "title_query": title_query,
    }

    return render(request, "achievements.html", context)

# VIEW GET ACHIEVEMENTS JSON
def get_achievements_json(request):
    title_query = request.GET.get("title", "").strip()

    achievements = Achievements.objects.all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)
    achievements_json = serializers.serialize("json", achievements)

    return HttpResponse(
        achievements_json,
        content_type="application/json"
    )


# VIEW DELETE ACHIEVEMENTS
def delete_achievements(request, achievements_id):
    achievement = get_object_or_404(Achievements, pk=achievements_id)
    if request.method == "POST":
        achievement.delete()
        messages.success(request,"Penghargaan berhasil dihapus!")
        return redirect("main:show_achievements")

    return redirect("main:show_achievements")


# UPDATE ACHIEVEMENTS
def update_achievements(request, achievements_id):
    achievement = get_object_or_404(Achievements,pk=achievements_id)

    form = AchievementsForm(request.POST or None, instance=achievement)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["secret_code"] != os.getenv("PORTOFOLIO_SECRET"):
            form.add_error(
                "secret_code",
                "TETOTT WKKWKWK Kode rahasia yang anda masukkan salah"
            )
        else:
            form.save()
            messages.success(request,"Penghargaan berhasil diperbarui!!")
            return redirect("main:show_achievements")

    context = {
        "name": "Alisa Selvia Saharani",
        "form": form,
        "achievement": achievement,
    }

    return render(
        request,
        "achievements_form.html",
        context
    )