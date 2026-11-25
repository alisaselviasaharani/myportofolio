from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
]

# URL API DRF (Tutorial 07)
urlpatterns += [
    path("api/v1/", include("main.api_urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/auth/token/", obtain_auth_token, name="api_token_auth"),
]
