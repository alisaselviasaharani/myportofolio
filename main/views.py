from django.shortcuts import render #import render dari django
# import model experience dan eduaction dari models.py
from main.models import Experience, Education

# VIEW PAGE HOME
def show_home(request):
    context={
        "name" : "Alisa Selvia Saharani",
        "perkenalan": "Hello, I'm Alisa",
        "bio": "I'm a Computer Science student at Universitas Indonesia.",
        "bio1":"Welcome to my portofolio!!!",
        "bio2":"This is a little space where I share more about myself.",
    }
    return render(request, "home.html",context)

# VIEW PAGE ABOUTME
def show_aboutme(request):
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

# VIEW PAGE EDUCATION
def show_education(request):
    context ={
        "name": "Alisa Selvia Saharani",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html",context)

# VIEW PAGE EXPERIENCE
def show_experience(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)