from django.test import TestCase
from django.urls import reverse
from main.models import Experience, Education


class MainTest(TestCase):
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

    def test_main_url_is_accessible(self):
        response = self.client.get(
            reverse("main:show_aboutme")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "aboutme.html")
        self.assertNotContains(
            response,
            self.experience.title
        )
        self.assertContains(
            response,
            f'href="{reverse("main:show_experience")}"'
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get(
            "/halaman-yang-tidak-ada/"
        )

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(
            str(self.experience),
            "Vice Chairperson of IT Club 65"
        )
        self.assertEqual(
            self.experience.category,
            "part-time"
        )
        self.assertEqual(
            self.experience.institution,
            "SMAN 65 JAKARTA"
        )
        self.assertEqual(
            self.experience.period,
            "2024-2025"
        )

    def test_experience_page(self):
        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "experience.html"
        )
        self.assertContains(
            response,
            self.experience.title
        )
        self.assertContains(
            response,
            self.experience.description
        )
        self.assertContains(
            response,
            "Part-Time"
        )
        self.assertContains(
            response,
            self.experience.institution
        )
        self.assertContains(
            response,
            self.experience.period
        )

    def test_empty_experience_page(self):
        Experience.objects.all().delete()

        response = self.client.get(
            reverse("main:show_experience")
        )

        self.assertContains(
            response,
            "Belum ada pengalaman yang ditambahkan."
        )

    # EDUCATION TEST

    def test_education_url_and_template(self):
        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "education.html"
        )

    def test_education_data_appears(self):
        education = Education.objects.create(
            institution="Universitas Indonesia",
            degree="S1 Ilmu Komputer",
            period="2025 - Present",
            logo="/static/img/logoUI.png",
            website="https://cs.ui.ac.id/",
        )

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertContains(
            response,
            education.institution
        )
        self.assertContains(
            response,
            education.degree
        )
        self.assertContains(
            response,
            education.period
        )

    def test_empty_education_page(self):
        Education.objects.all().delete()

        response = self.client.get(
            reverse("main:show_education")
        )

        self.assertContains(
            response,
            "Belum ada data pendidikan."
        )