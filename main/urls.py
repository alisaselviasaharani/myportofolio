from django.urls import path

from main.views import show_home, show_main, show_experience

app_name = "main"

urlpatterns = [
    path("", show_home, name="show_home"),
    path("aboutme/", show_main, name="aboutme"),
    path("experience/", show_experience, name="show_experience"),
]