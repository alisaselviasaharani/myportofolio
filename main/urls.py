from django.urls import path
from main.views import show_home, show_aboutme, show_experience, show_education

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
]