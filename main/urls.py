from django.urls import path
from main.views import show_home, show_aboutme, show_experience, show_education, show_achievements, create_achievements, get_achievements_json,delete_achievements, update_achievements

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
    
    path("achievements/", show_achievements, name="show_achievements"),

    path("achievements/add/", create_achievements, name="create_achievements"),

    path("api/achievements/", get_achievements_json, name="get_achievements_json"),

    path("achievements/<uuid:achievements_id>/delete/", delete_achievements, name="delete_achievements"),

    path("achievements/<uuid:achievements_id>/update/", update_achievements, name="update_achievements"),
]
