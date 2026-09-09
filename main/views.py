from django.shortcuts import render
from main.models import Experience

def show_home(request):
    return render(request, "home.html")

def show_main(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "npm": "2506618433",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Computer Science student at Universitas Indonesia who is interested in learning, "
            "exploring new things, and developing skills in technology and data."
        ),
    }

    return render(request, "aboutme.html", context)


def show_experience(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)