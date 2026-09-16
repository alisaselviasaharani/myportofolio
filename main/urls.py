from django.urls import path
from main.views import show_home, show_aboutme, show_experience, show_education, show_projects, create_project, get_projects_json,delete_project

# Memberikan namespace "main" untuk URL pada aplikasi main.
app_name = "main"

# Daftar seluruh URL yang tersedia pada aplikasi main.
urlpatterns = [
    # URL halaman Home.
    path("", show_home, name="show_home"),

    # URL halaman About Me.
    path("aboutme/", show_aboutme, name="show_aboutme"),

    # URL halaman Experience.
    path("experience/", show_experience, name="show_experience"),
    
    # URL halaman Education.
    path("education/", show_education, name="show_education"),
    
    path("projects/", show_projects, name="show_projects"),

    path("projects/add/", create_project, name="create_project"),


    path("api/projects/", get_projects_json, name="get_projects_json"),

    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
]