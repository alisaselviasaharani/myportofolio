from django.urls import path
from rest_framework.authtoken import views as authtoken_views
from main import api_views

# namespace "api" dipakai di reverse(), contoh: reverse("api:achievements-list")
app_name = "api"

# Pola URL-nya sama untuk ketiga resource:
#   <resource>/            -> list (GET) dan buat baru (POST)
#   <resource>/<id>/       -> detail (GET), ubah (PUT/PATCH), hapus (DELETE)
#   <resource>/<id>/star/  -> toggle star (POST, harus login)
urlpatterns = [
    # Achievements (primary key-nya UUID)
    path("achievements/", api_views.achievements_list, name="achievements-list"),
    path("achievements/<uuid:achievements_id>/", api_views.achievements_detail, name="achievements-detail"),
    path("achievements/<uuid:achievements_id>/star/", api_views.achievements_star, name="achievements-star"),

    # Experience (primary key-nya UUID)
    path("experience/", api_views.experience_list, name="experience-list"),
    path("experience/<uuid:experience_id>/", api_views.experience_detail, name="experience-detail"),
    path("experience/<uuid:experience_id>/star/", api_views.experience_star, name="experience-star"),

    # Education (primary key-nya integer biasa, makanya pakai <int:...>)
    path("education/", api_views.education_list, name="education-list"),
    path("education/<int:education_id>/", api_views.education_detail, name="education-detail"),
    path("education/<int:education_id>/star/", api_views.education_star, name="education-star"),

    # Autentikasi token untuk aplikasi Flutter (Tutorial 10)
    path("auth/token/", authtoken_views.obtain_auth_token, name="api_token_auth"),
    path("auth/logout/", api_views.api_logout, name="api_logout"),
]
