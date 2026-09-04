from django.contrib import admin
from django.urls import path

from portofolio.views import home_page
from portofolio.views import aboutme_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page, name='home'),
    path('about/', aboutme_page, name='aboutme'),
]