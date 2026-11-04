from django.urls import path

from main import api_views

app_name = "api"

urlpatterns = [
    # Achievements
    path("achievements/", api_views.achievements_list, name="achievements-list"),
    path("achievements/<uuid:achievements_id>/", api_views.achievements_detail, name="achievements-detail"),
    path("achievements/<uuid:achievements_id>/star/", api_views.achievements_star, name="achievements-star"),

    # Experience
    path("experience/", api_views.experience_list, name="experience-list"),
    path("experience/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experience/<uuid:experience_id>/star/", api_views.experience_star, name="experience-star"),
]
