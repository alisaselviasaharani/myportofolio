import os
import uuid
from unittest import mock

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Achievements, Experience

SECRET = "test-secret"


class ResourceAPITestMixin:
    """
    Pola uji yang sama untuk Achievements dan Experience.
    Subclass wajib mengisi: basename, model, create_kwargs, payload,
    patch_payload, invalid_field_case.
    """

    secret = {}  # tambahan field wajib saat menulis (Achievements: secret_code)

    def setUp(self):
        patcher = mock.patch.dict(os.environ, {"PORTOFOLIO_SECRET": SECRET})
        patcher.start()
        self.addCleanup(patcher.stop)

        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.obj = self.model.objects.create(**self.create_kwargs)

        self.list_url = reverse(f"api:{self.basename}-list")
        self.detail_url = reverse(f"api:{self.basename}-detail", args=[self.obj.id])
        self.star_url = reverse(f"api:{self.basename}-star", args=[self.obj.id])

    # ----- baca -----
    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.obj.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertNotIn("secret_code", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": self.create_kwargs["title"][:4].upper()})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_missing_object(self):
        url = reverse(f"api:{self.basename}-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    # ----- izin -----
    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, self.patch_payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, self.create_kwargs["title"])

    def test_staff_without_editor_group_cannot_write(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, self.patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_update_but_not_create_or_delete(self):
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(self.detail_url, self.patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(self.model.objects.count(), 1)

    # ----- tulis oleh pemilik -----
    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.model.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": " "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            self.invalid_field_case,
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(self.model.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.patch(self.detail_url, self.patch_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.title, self.patch_payload["title"])
        self.assertEqual(self.obj.description, self.create_kwargs["description"])  # tidak ikut berubah

        response = self.client.put(self.detail_url, {"title": "Incomplete", **self.secret}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(self.model.objects.filter(pk=self.obj.id).exists())

    # ----- star -----
    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    # ----- method & CSRF -----
    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.client.force_authenticate(user=self.visitor)
        self.assertEqual(self.client.get(self.star_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.model.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # Browsable API merender token CSRF sungguhan ke cookie.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AchievementsAPITest(ResourceAPITestMixin, APITestCase):
    basename = "achievements"
    model = Achievements
    secret = {"secret_code": SECRET}
    create_kwargs = {
        "title": "Dean's List", "description": "Top students", "category": "Academic",
    }
    payload = {
        "title": "New award", "description": "A useful award", "period": "2025",
        "category": "Award", "achievements_image_url": "https://example.com/a.png",
        **secret,
    }
    patch_payload = {"title": "Changed", **secret}
    invalid_field_case = ({"achievements_image_url": "javascript:alert(1)"}, "achievements_image_url")

    def test_secret_code_is_required_and_checked(self):
        self.client.force_authenticate(user=self.owner)
        without = {k: v for k, v in self.payload.items() if k != "secret_code"}
        for data in (without, {**self.payload, "secret_code": "salah"}):
            response = self.client.post(self.list_url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("secret_code", response.data)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.model.objects.count(), 1)


class ExperienceAPITest(ResourceAPITestMixin, APITestCase):
    basename = "experience"
    model = Experience
    create_kwargs = {
        "title": "IT Club Vice Chair", "description": "Assisted club activities",
        "category": "part-time", "institution": "SMAN 65 JAKARTA", "period": "2024-2025",
    }
    payload = {
        "title": "New experience", "description": "Did useful things", "category": "internship",
        "institution": "Example Corp", "period": "2025",
        "logo": "/static/img/logo.png", "website": "https://example.com/",
    }
    patch_payload = {"title": "Changed"}
    invalid_field_case = ({"website": "javascript:alert(1)"}, "website")

    def test_category_display_and_unsafe_logo(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.data["category"], "part-time")
        self.assertEqual(response.data["category_display"], "Part-Time")

        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            self.list_url, {**self.payload, "logo": "javascript:alert(1)"}, format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("logo", response.data)
