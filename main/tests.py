from django.test import TestCase
from django.urls import reverse
from main.models import Experience, Education


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
    def test_experience_page(self):
        #mengakses halaman experience
        response = self.client.get(reverse("main:show_experience"))

        #Memastikan page berhasil diakses (status code 200= berhasil)
        self.assertEqual(response.status_code, 200)

        #memastikan halaman menggunakan template aboutme.html
        self.assertTemplateUsed(response,"experience.html")

        # Memastikan judul Experience muncul pada halaman.
        self.assertContains(response,self.experience.title)

        # Memastikan  DESKRIPSI muncul pada halaman.
        self.assertContains(response, self.experience.description)

        # Memastikan kategori
        self.assertContains(response,"Part-Time")

        #memastikan institusi muncul
        self.assertContains(response,self.experience.institution)

        #memastikan periode muncul
        self.assertContains(response,self.experience.period)

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