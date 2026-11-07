from django.contrib import admin
from .models import Experience, Education, Contact,Skill
# Register your models here.


admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Contact)
admin.site.register(Skill)