from django.shortcuts import render


def show_home(request):
    return render(request,"home.html")

def show_aboutme(request):
    return render(request, "aboutme.html")

def show_experience(request):
    return render(request, "experience.html")
