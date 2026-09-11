from django.urls import path

from main.views import show_home, show_main, show_experience, show_education

app_name = "main"

urlpatterns = [
    path("", show_home, name="show_home"),
    path("aboutme/", show_main, name="aboutme"),
    path("experience/", show_experience, name="show_experience"),
    path("education/", show_education, name="show_education"),
]