import os
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Contact, Experience, Education, Achievements, Skill
from main.forms import AchievementsForm,ExperienceForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import HttpResponse, QueryDict
from django.views.decorators.http import require_http_methods

# VIEW PAGE HOME
def show_home(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "perkenalan": "Hello, I'm Alisa",
        "bio": "I'm a Computer Science student at Universitas Indonesia.",
        "bio1": "Welcome to my portofolio!!!",
        "bio2": "This is a little space where I share more about myself.",
        
    }

    return render(request, "home.html", context)

# VIEW PAGE ABOUTME
def show_aboutme(request):
    last_login = request.COOKIES.get(
        'last_login',
        'Belum ada sesi login / Cookie tidak ditemukan'
    )
    context = {
        "name": "Alisa Selvia Saharani",
        "npm": "2506618433",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Computer Science student at Universitas Indonesia who is interested "
            "in learning, exploring new things, and developing skills in technology and data."
        ),
        "last_login": last_login,
    }

    return render(request, "aboutme.html", context)


# VIEW PAGE EDUCATION
def show_education(request):
    context = {
        "name": "Alisa Selvia Saharani",
        "education_list": Education.objects.all(),
    }

    return render(request, "education.html", context)


# VIEW PAGE EXPERIENCE
def show_experience(request):
    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Alisa Selvia Saharani",
        "is_editor": is_editor,
        "form": ExperienceForm(),
    }

    return render(request, "experience.html", context)

# VIEW GET EXPERIENCE JSON
def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()

    experiences = Experience.objects.prefetch_related("starred_by").all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    data = []

    for experience in experiences:
        starred_users = experience.starred_by.all()
        is_starred = (
            request.user in starred_users
            if request.user.is_authenticated
            else False
        )

        data.append({
            "id": str(experience.id),
            "title": experience.title,
            "institution": experience.institution,
            "period": experience.period,
            "category": experience.get_category_display(),
            "description": experience.description,
            "logo": experience.logo,
            "website": experience.website,
            "star_count": starred_users.count(),
            "is_starred": is_starred,
        })

    return JsonResponse(data, safe=False)

@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {
                "message": "Hanya pemilik portofolio yang dapat menambahkan experience."
            },
            status=403,
        )

    form = ExperienceForm(request.POST)

    if form.is_valid():
        experience = form.save()

        return JsonResponse(
            {
                "message": "Experience berhasil ditambahkan.",
                "pk": str(experience.id),
            },
            status=201,
        )

    return JsonResponse(
        {
            "errors": form.errors.get_json_data()
        },
        status=400,
    )

# VIEW DELETE EXPERIENCE
@login_required(login_url="/login/")
@require_POST
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menghapus experience."},
            status=403,
        )

    experience = get_object_or_404(Experience, pk=experience_id)
    experience.delete()

    return JsonResponse(
        {"message": "Experience berhasil dihapus."},
        status=200,
    )

@require_POST
@login_required(login_url="/login/")
def update_experience_ajax(request, experience_id):
    is_editor = request.user.groups.filter(name="Editor").exists()

    if not request.user.is_superuser and not is_editor:
        return JsonResponse(
            {"message": "Anda tidak memiliki izin untuk memperbarui experience."},
            status=403,
        )

    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST, instance=experience)

    if form.is_valid():
        form.save()
        return JsonResponse(
            {"message": "Experience berhasil diperbarui."},
            status=200,
        )

    return JsonResponse(
        {"errors": form.errors.get_json_data()},
        status=400,
    )

# VIEW TOGGLE STAR EXPERIENCE
@login_required(login_url="/login/")
def toggle_star_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
            messages.success(request, "Kok dihapus starnya :(")
        else:
            experience.starred_by.add(request.user)
            messages.success(request, "Yeayy!! Anda berhasil menambahkan star >.<")

    return redirect("main:show_experience")

# VIEW PAGE CREATE ACHIEVEMENTS
@login_required(login_url="/login/")
def create_achievements(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    form = AchievementsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        if form.cleaned_data["secret_code"] != os.getenv("PORTOFOLIO_SECRET"):
            form.add_error(
                "secret_code",
                "TETOTT WKKWKWK Kode rahasia yang anda masukkan salah"
            )
        else:
            form.save()
            messages.success(
                request,
                "Penghargaan baru berhasil ditambahkan!"
            )
            return redirect("main:show_achievements")

    context = {
        "name": "Alisa Selvia Saharani",
        "form": form,
    }

    return render(request, "achievements_form.html", context)

# VIEW PAGE ACHIEVEMENTS
# def show_achievements(request):
#     title_query = request.GET.get("title", "").strip()

#     achievements = Achievements.objects.all()

#     if title_query:
#         achievements = achievements.filter(title__icontains=title_query)

#     # Serialize data menjadi JSON
#     achievements_json = serializers.serialize("json", achievements)

#     # Deserialize JSON kembali menjadi objek Django
#     achievements_data = list(serializers.deserialize("json", achievements_json))
#     is_editor = request.user.groups.filter(name="Editor").exists()
#     context = {
#         "name": "Alisa Selvia Saharani",
#         "achievements_list": achievements_data,
#         "title_query": title_query,
#         "is_editor":is_editor,
#         "form":AchievementsForm(),
#     }

#     return render(request, "achievements.html", context)
def show_achievements(request):
    is_editor = request.user.groups.filter(name="Editor").exists()

    context = {
        "name": "Alisa Selvia Saharani",
        "is_editor": is_editor,
        "form": AchievementsForm(),
    }

    return render(request, "achievements.html", context)

# VIEW GET ACHIEVEMENTS JSON
def get_achievements_json(request):
    title_query = request.GET.get("title", "").strip()

    # achievements = Achievements.objects.all()
    achievements=Achievements.objects.prefetch_related('starred_by').all()

    if title_query:
        achievements = achievements.filter(title__icontains=title_query)

    data=[]
    for achievement in achievements:
        starred_users = achievement.starred_by.all()
        is_starred = (request.user in starred_users if request.user.is_authenticated else False)
        data.append({
                    "id": str(achievement.id),
                        "title": achievement.title,
                        "description": achievement.description,
                        "category": achievement.category,
                        # "achievements_image_url": achievement.achievements_image_url,
                        "star_count": starred_users.count(),
                        "is_starred": is_starred,
                })

    return JsonResponse(data, safe=False)

# VIEW DELETE ACHIEVEMENTS
@login_required(login_url="/login/")
def delete_achievements(request, achievements_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    achievement = get_object_or_404(Achievements, pk=achievements_id)
    if request.method == "POST":
        achievement.delete()
        messages.success(request,"Penghargaan berhasil dihapus!")
        return redirect("main:show_achievements")

    return redirect("main:show_achievements")


# UPDATE ACHIEVEMENTS
@login_required(login_url="/login/")
def update_achievements(request, achievements_id):
    is_editor=request.user.groups.filter(name="Editor").exists()
    if not request.user.is_superuser and not is_editor:
        raise PermissionDenied

    achievement = get_object_or_404(
        Achievements,
        pk=achievements_id
    )

    if request.method == "POST":
        form = AchievementsForm(
            request.POST,
            instance=achievement
        )

        if form.is_valid():
            if form.cleaned_data["secret_code"] != os.getenv("PORTOFOLIO_SECRET"):
                form.add_error(
                    "secret_code",
                    "TETOTT WKKWKWK Kode rahasia yang anda masukkan salah"
                )
            else:
                form.save()
                messages.success(request,"Penghargaan berhasil diperbarui!!")
                return redirect("main:show_achievements")
    else:
        form = AchievementsForm(
            instance=achievement
        )

    context = {
        "name": "Alisa Selvia Saharani",
        "form": form,
        "achievement": achievement,
    }

    return render(
        request,
        "achievements_form.html",
        context
    )
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Alisa Selvia Saharani",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request,"Selamat Anda Telah Berhasil Login ke Website milik Alisa Selvia Saharani :)")
        response = redirect("main:show_aboutme")
        response.set_cookie(
            "last_login",
            timezone.localtime().strftime("%d %B %Y, %H:%M:%S")
        )
        return response

    context = {
        "name": "Alisa Selvia Saharani",
        "form": form,
    }

    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    messages.success(request, "Yeayy!! Selamat Anda Sudah Logout!!")
    response = redirect("main:show_home")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, achievements_id):
    achievement = get_object_or_404(
        Achievements,
        pk=achievements_id
    )

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in achievement.starred_by.all():
            achievement.starred_by.remove(request.user)
            messages.success(request,"Kok dihapus starnya :(")
        else:
            achievement.starred_by.add(request.user)
            messages.success(request,"Yeayy!! Anda berhasil menambahkan star >.<")

    return redirect("main:show_achievements")

@require_POST
def create_achievements_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = AchievementsForm(request.POST)
    if form.is_valid():
        if form.cleaned_data["secret_code"] != os.getenv("PORTOFOLIO_SECRET"):
            form.add_error(
                "secret_code",
                "Kode rahasia yang anda masukkan salah."
            )
            
        else:
            achievement = form.save()
            return JsonResponse(
                {"message": "Penghargaan berhasil ditambahkan.", "pk": str(achievement.id)},
                status=201,
            )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def contact_add(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
        )
    contacts = Contact.objects.all()
    return render(request, "_contact_rows.html", {"contacts": contacts})

def contact_search(request):
    query = request.GET.get("q", "")
    contacts = Contact.objects.filter(name__icontains=query) if query else Contact.objects.all()
    return render(request, "_contact_rows.html", {"contacts": contacts})

@require_http_methods(["DELETE"])
def contact_delete(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    contact.delete()
    return HttpResponse("")

def contact_list(request):
    contacts=Contact.objects.all()
    return render (request, "index.html", {"contacts":contacts})

def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "_contact_edit_row.html", {"contact": contact})

def contact_row(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(request, "_contact_row.html", {"contact": contact})

@require_http_methods(["PUT"])
def contact_update(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    data = QueryDict(request.body)
    contact.name = data.get("name", contact.name)
    contact.email = data.get("email", contact.email)
    contact.save()
    return render(request, "_contact_row.html", {"contact": contact})

def show_skills(request):
    hard_skills = Skill.objects.filter(jenis='Hard Skill')
    soft_skills = Skill.objects.filter(jenis='Soft Skill')
    context = {
        'hard_skills': hard_skills,
        'soft_skills': soft_skills,
    }
    return render(request, 'skills.html', context)