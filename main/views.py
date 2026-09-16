from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render #import render dari django
# import model experience dan eduaction dari models.py
from main.models import Experience, Education, Project
from main.forms import ProjectForm

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


def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "projects_form.html", context)


def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")