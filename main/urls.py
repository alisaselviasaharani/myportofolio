from django.urls import path
from main.views import (
    show_home,
    show_aboutme,
    show_experience,
    show_education,
    show_achievements,
    create_achievements,
    get_achievements_json,
    delete_achievements,
    delete_experience,
    update_achievements,
    login_user,
    logout_user,
    register,
    toggle_star,
    create_achievements_ajax,
    get_experience_json,
    create_experience_ajax,
    toggle_star_experience,
    update_experience_ajax,
)

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

    # URL JSON Experience untuk AJAX.
    path("api/experience/", get_experience_json, name="get_experience_json"),

    # URL tambah Experience melalui AJAX.
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),

    # URL hapus Experience.
    path("experience/<uuid:experience_id>/delete/", delete_experience, name="delete_experience"),

    # URL halaman Education.
    path("education/", show_education, name="show_education"),

    # URL halaman Achievements.
    path("achievements/", show_achievements, name="show_achievements"),
    path("achievements/add/", create_achievements, name="create_achievements"),
    path("api/achievements/", get_achievements_json, name="get_achievements_json"),
    path("achievements/<uuid:achievements_id>/delete/", delete_achievements, name="delete_achievements"),
    path("achievements/<uuid:achievements_id>/update/", update_achievements, name="update_achievements"),
    path("achievements/<uuid:achievements_id>/star/", toggle_star, name="toggle_star"),

    # URL register, login, logout.
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    # URL tambah Achievements melalui AJAX.
    path("achievements/add-ajax/", create_achievements_ajax, name="create_achievements_ajax"),

    path("experience/<uuid:experience_id>/star/",toggle_star_experience,name="toggle_star_experience"),
    path("experience/<uuid:experience_id>/update-ajax/", update_experience_ajax, name="update_experience_ajax"),
]