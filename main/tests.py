import os
from unittest import mock

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from main.forms import AchievementsForm, ExperienceForm
from main.models import Achievements, Contact, Education, Experience


class MainTest(TestCase):
    # --------->>>>> SETUP EXPERIENCE TEST <<<<<---------
    # Note: menguji data yang saya punya dengan beberapa test
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Vice Chairperson of IT Club 65",
            description="Assisted in coordinating IT Club activities and supporting members in learning and developing their technology skills.",
            category="part-time",
            institution="SMAN 65 JAKARTA",
            period="2024-2025",
            logo="/static/img/logoIT65.png",
            website="https://www.youtube.com/@itclubsman6575/videos",
        )

    # Test URL dan TEMPLATE
    def test_main_url_is_accessible(self):
        #Mengakses page about me dengan url
        response = self.client.get(reverse("main:show_aboutme"))

        #Memastikan page berhasil diakses (status code 200= berhasil)
        self.assertEqual(response.status_code, 200)

        #memastikan halaman menggunakan template aboutme.html
        self.assertTemplateUsed(response, "aboutme.html")

        #menuju link page experience
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    # Test halaman tdk ada
    def test_nonexistent_page_returns_404(self):
        #mencoba akses halaman yg tdk tersedia
        response = self.client.get("/halaman-yang-tidak-ada/")

        #Memastikan django statusnya 404 
        self.assertEqual(response.status_code, 404)

    # Test model experince
    def test_experience_model(self):
        # mengembalikan judul Experience.
        self.assertEqual(str(self.experience),"Vice Chairperson of IT Club 65")

        # Memastikan kategori Experience tersimpan dengan benar.
        self.assertEqual(self.experience.category,"part-time")

        # Memastikan institution tersimpan dengan benar.
        self.assertEqual(self.experience.institution,"SMAN 65 JAKARTA")

        # Memastikan period tersimpan dengan benar
        self.assertEqual(self.experience.period,"2024-2025")

    # Test halaman experience
    # Note: sejak Tutorial 05 kartu dirender oleh JavaScript dari API, jadi HTML server
    # tidak lagi memuat judulnya. Yang diuji: halaman memuat endpoint API DRF dan
    # API mengembalikan data experience yang sama.
    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")

        # Halaman memanggil endpoint DRF
        self.assertContains(response, reverse("api:experience-list"))

        # Data experience tersedia lewat API
        data = self.client.get(reverse("api:experience-list")).json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], self.experience.title)
        self.assertEqual(data[0]["description"], self.experience.description)
        self.assertEqual(data[0]["category_display"], "Part-Time")
        self.assertEqual(data[0]["institution"], self.experience.institution)
        self.assertEqual(data[0]["period"], self.experience.period)

    # Test empty state experience
    def test_empty_experience_page(self):
        # Menghapus seluruuh data experiece dari data base
        Experience.objects.all().delete()

        # akses halaman self.experience setelah data base kosong
        response = self.client.get(reverse("main:show_experience"))

        # memastikan pesan empty state di tampilkan
        self.assertContains(response,"Belum ada pengalaman yang ditambahkan.")

    # --------->>>>> SETUP EDUCATION TEST <<<<<---------
    def test_education_data_appears(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            period="2025 - Present",
            logo="/static/img/logoUI.png",
            website="https://cs.ui.ac.id/",
        )
        #mengakses halaman education
        response = self.client.get(reverse("main:show_education"))

        #cek institusi muncul
        self.assertContains( response,education.institution)

        #cek jurusan 
        self.assertContains(response, education.degree)

        #cek periode pendidikan
        self.assertContains(response,education.period)

    # Test URL dan TEMPLATE
    def test_education_url_and_template(self):
        # Mengakses halaman Education menggunakan nama URL.
        response = self.client.get(reverse("main:show_education"))

        #Memastikan page berhasil diakses (status code 200= berhasil)
        self.assertEqual(response.status_code, 200)

        #memastikan halaman menggunakan template education.html
        self.assertTemplateUsed(response,"education.html")

    # Test Page Education
    def test_empty_education_page(self):
        # Menghapus seluruh data Education dari database test.
        Education.objects.all().delete()

        # Mengakses halaman Education setelah database kosong
        response = self.client.get(reverse("main:show_education"))

        # Memastikan pesan empty state ditampilkan.
        self.assertContains(response,"Belum ada data pendidikan.")



# TEST TAMBAHAN UNTUK SELURUH TUGAS (Tugas 1 - 6)

SECRET = "rahasia-test"
STRONG_PASSWORD = "Str0ng-Pass-2026"


class BaseSiteTestCase(TestCase):
    """Data & akun dasar: pemilik (superuser), Editor, dan pengunjung biasa."""

    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"PORTOFOLIO_SECRET": SECRET})
        patcher.start()
        self.addCleanup(patcher.stop)

        self.owner = User.objects.create_superuser("owner", "owner@example.com", "test-password")
        self.editor = User.objects.create_user("editor", password="test-password")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user("visitor", password="test-password")

        self.achievement = Achievements.objects.create(
            title="Juara 1 Lomba", description="Lomba web", category="Competition", period="2025",
        )
        self.experience = Experience.objects.create(
            title="Asisten Lab", description="Membantu praktikum", category="part-time",
            institution="Fasilkom UI", period="2025",
        )

    def login(self, user):
        self.assertTrue(self.client.login(username=user.username, password="test-password"))

    def achievement_data(self, **changes):
        data = {
            "title": "Penghargaan Baru", "period": "2026", "description": "Deskripsi",
            "category": "Award", "achievements_image_url": "", "secret_code": SECRET,
        }
        data.update(changes)
        return data

    def experience_data(self, **changes):
        data = {
            "title": "Magang", "institution": "PT Contoh", "period": "2026",
            "category": "internship", "description": "Belajar banyak",
            "logo": "", "website": "",
        }
        data.update(changes)
        return data


# --------->>>>> TUGAS 1-2: HALAMAN & MODEL <<<<<---------
class PagesAndModelsTest(BaseSiteTestCase):
    def test_public_pages_are_accessible(self):
        for name, template in [
            ("main:show_home", "home.html"),
            ("main:show_aboutme", "aboutme.html"),
            ("main:show_experience", "experience.html"),
            ("main:show_education", "education.html"),
            ("main:show_achievements", "achievements.html"),
            ("main:login", "login.html"),
            ("main:register", "register.html"),
        ]:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_aboutme_shows_profile(self):
        response = self.client.get(reverse("main:show_aboutme"))
        self.assertContains(response, "Alisa Selvia Saharani")
        self.assertContains(response, "2506618433")

    def test_model_str_and_uuid_primary_keys(self):
        self.assertEqual(str(self.achievement), "Juara 1 Lomba")
        self.assertEqual(str(self.experience), "Asisten Lab")
        self.assertEqual(str(Contact.objects.create(name="Budi", email="budi@example.com")), "Budi")
        self.assertEqual(str(Education.objects.create(
            institution="UI", degree="S1", period="2025", logo="/l.png", website="https://ui.ac.id")), "UI")
        self.assertEqual(len(str(self.achievement.id)), 36)
        self.assertEqual(len(str(self.experience.id)), 36)

    def test_achievements_page_uses_drf_endpoints(self):
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, reverse("api:achievements-list"))
        self.assertContains(response, "Belum ada penghargaan yang ditambahkan atau ditemukan.")
        # modal tambah hanya untuk superuser
        self.assertNotContains(response, 'id="add-achievements-modal"')
        self.login(self.owner)
        response = self.client.get(reverse("main:show_achievements"))
        self.assertContains(response, 'id="add-achievements-modal"')

    def test_experience_form_modal_has_all_fields(self):
        response = self.client.get(reverse("main:show_experience"))
        for field in ("title", "institution", "period", "category", "description", "logo", "website"):
            self.assertContains(response, f'name="{field}"')


# --------->>>>> TUGAS 3: FORM, CRUD ACHIEVEMENTS <<<<<---------
class FormsTest(BaseSiteTestCase):
    def test_experience_form_strips_tags_and_rejects_empty(self):
        form = ExperienceForm(self.experience_data(title="<b>Magang</b>", description="<i>Seru</i>"))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Magang")
        self.assertEqual(form.cleaned_data["description"], "Seru")

        form = ExperienceForm(self.experience_data(title="<img src=x onerror=alert(1)>"))
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

        form = ExperienceForm(self.experience_data(description="<p></p>"))
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def test_achievements_form_requires_secret_code_and_strips_tags(self):
        data = self.achievement_data(title="<b>Hebat</b>", description="<i>Bagus</i>")
        form = AchievementsForm(data)
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Hebat")
        self.assertEqual(form.cleaned_data["description"], "Bagus")

        data.pop("secret_code")
        form = AchievementsForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn("secret_code", form.errors)

        form = AchievementsForm(self.achievement_data(title="<img src=x>"))
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class AchievementsCrudViewsTest(BaseSiteTestCase):
    def test_create_page_permissions(self):
        url = reverse("main:create_achievements")
        response = self.client.get(url)
        self.assertRedirects(response, f"/login/?next={url}", fetch_redirect_response=False)

        self.login(self.visitor)
        self.assertEqual(self.client.get(url).status_code, 403)

        self.client.logout()
        self.login(self.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "achievements_form.html")

    def test_owner_creates_with_correct_secret(self):
        self.login(self.owner)
        response = self.client.post(reverse("main:create_achievements"),
                                    self.achievement_data(title="<b>Dibuat</b>"))
        self.assertRedirects(response, reverse("main:show_achievements"), fetch_redirect_response=False)
        self.assertTrue(Achievements.objects.filter(title="Dibuat").exists())

    def test_wrong_secret_does_not_create(self):
        self.login(self.owner)
        response = self.client.post(reverse("main:create_achievements"),
                                    self.achievement_data(secret_code="salah"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("secret_code", response.context["form"].errors)
        self.assertEqual(Achievements.objects.count(), 1)

    def test_update_allowed_for_owner_and_editor_only(self):
        url = reverse("main:update_achievements", args=[self.achievement.id])

        self.login(self.visitor)
        self.assertEqual(self.client.post(url, self.achievement_data(title="Hack")).status_code, 403)
        self.client.logout()

        for user, title in ((self.editor, "Diubah Editor"), (self.owner, "Diubah Owner")):
            self.login(user)
            response = self.client.post(url, self.achievement_data(title=title))
            self.assertRedirects(response, reverse("main:show_achievements"), fetch_redirect_response=False)
            self.achievement.refresh_from_db()
            self.assertEqual(self.achievement.title, title)
            self.client.logout()

    def test_update_with_wrong_secret_changes_nothing(self):
        self.login(self.editor)
        url = reverse("main:update_achievements", args=[self.achievement.id])
        response = self.client.post(url, self.achievement_data(title="Hack", secret_code="salah"))
        self.assertEqual(response.status_code, 200)
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Juara 1 Lomba")

    def test_update_page_prefills_form(self):
        self.login(self.editor)
        response = self.client.get(reverse("main:update_achievements", args=[self.achievement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Juara 1 Lomba")

    def test_delete_only_owner_and_only_post(self):
        url = reverse("main:delete_achievements", args=[self.achievement.id])

        self.login(self.visitor)
        self.assertEqual(self.client.post(url).status_code, 403)
        self.client.logout()
        self.login(self.editor)
        self.assertEqual(self.client.post(url).status_code, 403)
        self.client.logout()
        self.assertEqual(Achievements.objects.count(), 1)

        self.login(self.owner)
        self.client.get(url)  # GET tidak menghapus
        self.assertEqual(Achievements.objects.count(), 1)
        self.client.post(url)
        self.assertEqual(Achievements.objects.count(), 0)


# --------->>>>> TUGAS 4: AUTENTIKASI, COOKIE, STAR, PERAN <<<<<---------
class AuthenticationTest(BaseSiteTestCase):
    def test_register_creates_user(self):
        response = self.client.post(reverse("main:register"), {
            "username": "baru", "password1": STRONG_PASSWORD, "password2": STRONG_PASSWORD,
        })
        self.assertRedirects(response, reverse("main:login"), fetch_redirect_response=False)
        self.assertTrue(User.objects.filter(username="baru").exists())

    def test_register_with_mismatched_passwords_fails(self):
        response = self.client.post(reverse("main:register"), {
            "username": "baru", "password1": STRONG_PASSWORD, "password2": "beda-sekali-2026",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="baru").exists())

    def test_login_sets_last_login_cookie(self):
        response = self.client.post(reverse("main:login"),
                                    {"username": "visitor", "password": "test-password"})
        self.assertRedirects(response, reverse("main:show_aboutme"), fetch_redirect_response=False)
        self.assertIn("last_login", response.cookies)
        self.assertNotEqual(response.cookies["last_login"].value, "")
        self.assertEqual(self.client.session["_auth_user_id"], str(self.visitor.pk))

    def test_login_with_wrong_password_fails(self):
        response = self.client.post(reverse("main:login"),
                                    {"username": "visitor", "password": "salah"})
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_clears_session_and_cookie(self):
        self.login(self.visitor)
        self.client.cookies["last_login"] = "01 January 2026"
        response = self.client.get(reverse("main:logout"))
        self.assertRedirects(response, reverse("main:show_home"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)
        self.assertEqual(response.cookies["last_login"].value, "")

    def test_aboutme_shows_last_login_cookie_or_default(self):
        response = self.client.get(reverse("main:show_aboutme"))
        self.assertContains(response, "Belum ada sesi login")
        self.client.cookies["last_login"] = "01 January 2026"
        response = self.client.get(reverse("main:show_aboutme"))
        self.assertContains(response, "01 January 2026")


class StarViewsTest(BaseSiteTestCase):
    def test_achievement_star_requires_login(self):
        url = reverse("main:toggle_star", args=[self.achievement.id])
        response = self.client.post(url)
        self.assertRedirects(response, f"/login/?next={url}", fetch_redirect_response=False)
        self.assertEqual(self.achievement.starred_by.count(), 0)

    def test_achievement_star_toggles_per_user(self):
        url = reverse("main:toggle_star", args=[self.achievement.id])
        self.login(self.visitor)
        response = self.client.post(url)
        self.assertRedirects(response, reverse("main:show_achievements"), fetch_redirect_response=False)
        self.assertEqual(self.achievement.starred_by.count(), 1)
        self.client.post(url)
        self.assertEqual(self.achievement.starred_by.count(), 0)

        self.client.post(url)
        self.client.logout()
        self.login(self.editor)
        self.client.post(url)
        self.assertEqual(self.achievement.starred_by.count(), 2)

    def test_get_does_not_change_star(self):
        self.login(self.visitor)
        self.client.get(reverse("main:toggle_star", args=[self.achievement.id]))
        self.assertEqual(self.achievement.starred_by.count(), 0)

    def test_experience_star_requires_login_and_toggles(self):
        url = reverse("main:toggle_star_experience", args=[self.experience.id])
        self.client.post(url)
        self.assertEqual(self.experience.starred_by.count(), 0)

        self.login(self.visitor)
        response = self.client.post(url)
        self.assertRedirects(response, reverse("main:show_experience"), fetch_redirect_response=False)
        self.assertEqual(self.experience.starred_by.count(), 1)
        self.client.post(url)
        self.assertEqual(self.experience.starred_by.count(), 0)


class EditorRoleContextTest(BaseSiteTestCase):
    def test_is_editor_flag_on_pages(self):
        for name in ("main:show_experience", "main:show_achievements"):
            with self.subTest(page=name):
                self.login(self.editor)
                self.assertTrue(self.client.get(reverse(name)).context["is_editor"])
                self.client.logout()
                self.login(self.visitor)
                self.assertFalse(self.client.get(reverse(name)).context["is_editor"])
                self.client.logout()


# --------->>>>> TUGAS 5: ENDPOINT JSON & AJAX (versi JsonResponse) <<<<<---------
class LegacyJsonEndpointsTest(BaseSiteTestCase):
    def test_achievements_json_list_search_and_star_flag(self):
        self.achievement.starred_by.add(self.visitor)
        data = self.client.get(reverse("main:get_achievements_json")).json()
        self.assertEqual(data[0]["id"], str(self.achievement.id))
        self.assertEqual(data[0]["star_count"], 1)
        self.assertFalse(data[0]["is_starred"])

        self.login(self.visitor)
        self.assertTrue(self.client.get(reverse("main:get_achievements_json")).json()[0]["is_starred"])

        url = reverse("main:get_achievements_json")
        self.assertEqual(len(self.client.get(url, {"title": "JUARA"}).json()), 1)
        self.assertEqual(self.client.get(url, {"title": "tidak-ada"}).json(), [])

    def test_experience_json_fields_and_search(self):
        url = reverse("main:get_experience_json")
        data = self.client.get(url).json()
        self.assertEqual(data[0]["title"], "Asisten Lab")
        self.assertEqual(data[0]["category"], "Part-Time")
        self.assertEqual(data[0]["institution"], "Fasilkom UI")
        self.assertEqual(len(self.client.get(url, {"title": "asisten"}).json()), 1)
        self.assertEqual(self.client.get(url, {"title": "zzz"}).json(), [])


class AchievementsAjaxTest(BaseSiteTestCase):
    def setUp(self):
        super().setUp()
        self.url = reverse("main:create_achievements_ajax")

    def test_only_post_allowed(self):
        self.login(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_guest_and_visitor_forbidden(self):
        self.assertEqual(self.client.post(self.url, self.achievement_data()).status_code, 403)
        self.login(self.visitor)
        self.assertEqual(self.client.post(self.url, self.achievement_data()).status_code, 403)
        self.assertEqual(Achievements.objects.count(), 1)

    def test_owner_creates_with_secret(self):
        self.login(self.owner)
        response = self.client.post(self.url, self.achievement_data(title="<b>Ajax</b>"))
        self.assertEqual(response.status_code, 201)
        created = Achievements.objects.get(pk=response.json()["pk"])
        self.assertEqual(created.title, "Ajax")

    def test_wrong_secret_and_invalid_input_return_400(self):
        self.login(self.owner)
        response = self.client.post(self.url, self.achievement_data(secret_code="salah"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("secret_code", response.json()["errors"])

        response = self.client.post(self.url, self.achievement_data(title="<img src=x>"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])
        self.assertEqual(Achievements.objects.count(), 1)


class ExperienceAjaxTest(BaseSiteTestCase):
    def test_create_permissions_and_validation(self):
        url = reverse("main:create_experience_ajax")
        self.assertEqual(self.client.post(url, self.experience_data()).status_code, 403)

        for user in (self.visitor, self.editor):  # Editor tidak boleh membuat
            self.login(user)
            self.assertEqual(self.client.post(url, self.experience_data()).status_code, 403)
            self.client.logout()
        self.assertEqual(Experience.objects.count(), 1)

        self.login(self.owner)
        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url, self.experience_data(title="<b>Magang Baru</b>"))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Experience.objects.get(pk=response.json()["pk"]).title, "Magang Baru")

        response = self.client.post(url, self.experience_data(title="<i></i>"))
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.json()["errors"])

    def test_update_allowed_for_owner_and_editor(self):
        url = reverse("main:update_experience_ajax", args=[self.experience.id])

        self.assertEqual(self.client.post(url, self.experience_data()).status_code, 302)  # ke login

        self.login(self.visitor)
        self.assertEqual(self.client.post(url, self.experience_data(title="Hack")).status_code, 403)
        self.client.logout()

        self.login(self.editor)
        self.assertEqual(self.client.get(url).status_code, 405)
        response = self.client.post(url, self.experience_data(title="Diubah Editor"))
        self.assertEqual(response.status_code, 200)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Diubah Editor")

        response = self.client.post(url, self.experience_data(title=" "))
        self.assertEqual(response.status_code, 400)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Diubah Editor")

    def test_delete_only_owner(self):
        url = reverse("main:delete_experience", args=[self.experience.id])
        self.assertEqual(self.client.post(url).status_code, 302)  # ke login

        for user in (self.visitor, self.editor):
            self.login(user)
            self.assertEqual(self.client.post(url).status_code, 403)
            self.client.logout()
        self.assertEqual(Experience.objects.count(), 1)

        self.login(self.owner)
        self.assertEqual(self.client.get(url).status_code, 405)
        self.assertEqual(self.client.post(url).status_code, 200)
        self.assertEqual(Experience.objects.count(), 0)


# --------->>>>> Tutorial 6 (HTMX): KONTAK <<<<<---------
class ContactHtmxTest(BaseSiteTestCase):
    def setUp(self):
        super().setUp()
        self.contact = Contact.objects.create(name="Budi", email="budi@example.com")

    def test_list_and_search(self):
        response = self.client.get(reverse("main:contact_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Budi")

        response = self.client.get(reverse("main:contact_search"), {"q": "bud"})
        self.assertContains(response, "Budi")
        response = self.client.get(reverse("main:contact_search"), {"q": "zzz"})
        self.assertContains(response, "Tidak ada kontak.")

    def test_add_returns_rows_partial(self):
        response = self.client.post(reverse("main:contact_add"),
                                    {"name": "Sari", "email": "sari@example.com"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "_contact_rows.html")
        self.assertContains(response, "Sari")
        self.assertEqual(Contact.objects.count(), 2)

    def test_edit_row_update_and_delete(self):
        response = self.client.get(reverse("main:contact_edit", args=[self.contact.pk]))
        self.assertTemplateUsed(response, "_contact_edit_row.html")
        response = self.client.get(reverse("main:contact_row", args=[self.contact.pk]))
        self.assertTemplateUsed(response, "_contact_row.html")

        response = self.client.put(
            reverse("main:contact_update", args=[self.contact.pk]),
            "name=Baru&email=baru%40example.com",
            content_type="application/x-www-form-urlencoded",
        )
        self.assertEqual(response.status_code, 200)
        self.contact.refresh_from_db()
        self.assertEqual((self.contact.name, self.contact.email), ("Baru", "baru@example.com"))

        delete_url = reverse("main:contact_delete", args=[self.contact.pk])
        self.assertEqual(self.client.get(delete_url).status_code, 405)
        self.assertEqual(self.client.delete(delete_url).status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)


# --------->>>>> TUGAS 6: DRF API TESTS UNTUK EXPERIENCE & ACHIEVEMENTS <<<<<---------
class PortfolioSectionAPITest(APITestCase):
    """Menguji API DRF untuk empat peran sesuai rubrik Individual Assignment 6."""

    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"PORTOFOLIO_SECRET": SECRET})
        patcher.start()
        self.addCleanup(patcher.stop)
        self.owner = User.objects.create_superuser("api_owner", "owner@example.com", "pass12345")
        self.editor = User.objects.create_user("api_editor", password="pass12345")
        self.editor.groups.add(Group.objects.create(name="Editor"))
        self.visitor = User.objects.create_user("api_visitor", password="pass12345")
        self.exp = Experience.objects.create(
            title="Asisten Lab", institution="Fasilkom UI", period="2025",
            category="part-time", description="Membantu praktikum",
        )
        self.achievement = Achievements.objects.create(
            title="Juara Lomba", period="2025", description="Lomba pemrograman",
            category="Competition",
        )
        self.exp_list = reverse("api:experience-list")
        self.exp_detail = reverse("api:experience-detail", args=[self.exp.id])
        self.exp_star = reverse("api:experience-star", args=[self.exp.id])
        self.ach_list = reverse("api:achievements-list")
        self.ach_detail = reverse("api:achievements-detail", args=[self.achievement.id])
        self.ach_star = reverse("api:achievements-star", args=[self.achievement.id])

    def exp_payload(self, **kwargs):
        data = {"title": "Pengalaman Baru", "institution": "PT Contoh", "period": "2026",
                "category": "internship", "description": "Belajar Django", "logo": "", "website": ""}
        data.update(kwargs)
        return data

    def ach_payload(self, **kwargs):
        data = {"title": "Penghargaan Baru", "period": "2026", "description": "Deskripsi",
                "category": "Award", "achievements_image_url": "", "secret_code": SECRET}
        data.update(kwargs)
        return data

    def test_public_read_and_guest_write_denied_for_both_sections(self):
        for url in (self.exp_list, self.ach_list, self.exp_detail, self.ach_detail):
            self.assertEqual(self.client.get(url).status_code, 200)
        for url, payload in ((self.exp_list, self.exp_payload()), (self.ach_list, self.ach_payload())):
            self.assertEqual(self.client.post(url, payload, format="json").status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(Achievements.objects.count(), 1)

    def test_regular_user_cannot_write_but_can_star(self):
        self.client.force_authenticate(self.visitor)
        for url, payload in ((self.exp_list, self.exp_payload()), (self.ach_list, self.ach_payload())):
            self.assertEqual(self.client.post(url, payload, format="json").status_code, 403)
        self.assertEqual(self.client.patch(self.exp_detail, {"title": "Hack"}, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.ach_detail).status_code, 403)
        self.assertEqual(self.client.post(self.exp_star).status_code, 200)
        self.assertEqual(self.client.post(self.ach_star).status_code, 200)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(Achievements.objects.count(), 1)
        self.assertTrue(self.exp.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertTrue(self.achievement.starred_by.filter(pk=self.visitor.pk).exists())

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        self.client.force_authenticate(self.editor)
        self.assertEqual(self.client.post(self.exp_list, self.exp_payload(), format="json").status_code, 403)
        self.assertEqual(self.client.post(self.ach_list, self.ach_payload(), format="json").status_code, 403)
        self.assertEqual(self.client.patch(self.exp_detail, {"title": "Experience Diedit"}, format="json").status_code, 200)
        # PATCH achievement tidak meminta secret_code karena kode hanya untuk create.
        self.assertEqual(self.client.patch(self.ach_detail, {"title": "Achievement Diedit"}, format="json").status_code, 200)
        self.assertEqual(self.client.delete(self.exp_detail).status_code, 403)
        self.assertEqual(self.client.delete(self.ach_detail).status_code, 403)
        self.exp.refresh_from_db(); self.achievement.refresh_from_db()
        self.assertEqual(self.exp.title, "Experience Diedit")
        self.assertEqual(self.achievement.title, "Achievement Diedit")
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(Achievements.objects.count(), 1)

    def test_owner_can_create_update_and_delete_both_sections(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.exp_list, self.exp_payload(title="Experience Owner"), format="json")
        self.assertEqual(response.status_code, 201)
        new_exp_id = response.data["id"]
        response = self.client.post(self.ach_list, self.ach_payload(title="Achievement Owner"), format="json")
        self.assertEqual(response.status_code, 201)
        new_ach_id = response.data["id"]
        self.assertEqual(self.client.put(reverse("api:experience-detail", args=[new_exp_id]), self.exp_payload(title="Updated"), format="json").status_code, 200)
        self.assertEqual(self.client.delete(reverse("api:experience-detail", args=[new_exp_id])).status_code, 204)
        self.assertEqual(self.client.delete(reverse("api:achievements-detail", args=[new_ach_id])).status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=new_exp_id).exists())
        self.assertFalse(Achievements.objects.filter(pk=new_ach_id).exists())

    def test_validation_and_search(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.exp_list, self.exp_payload(title="<script></script>"), format="json")
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.ach_list, self.ach_payload(secret_code="salah"), format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get(self.exp_list + "?title=Asisten").data[0]["title"], "Asisten Lab")
        self.assertEqual(self.client.get(self.ach_list + "?title=Juara").data[0]["title"], "Juara Lomba")

    def test_star_rejects_guest(self):
        self.assertEqual(self.client.post(self.exp_star).status_code, 403)
        self.assertEqual(self.client.post(self.ach_star).status_code, 403)

    def test_session_authentication_rejects_missing_csrf_token(self):
        csrf_client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(csrf_client.login(username="api_owner", password="pass12345"))
        response = csrf_client.post(self.exp_list, self.exp_payload(), format="json")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
