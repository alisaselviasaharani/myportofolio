import os
import secrets

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievements, Experience


def _is_safe_url(value, allow_relative=False):
    """URL kosong, http(s), atau (opsional) path relatif seperti /static/img/a.png."""
    if not value:
        return True
    if value.startswith(("http://", "https://")):
        return True
    return allow_relative and value.startswith("/") and not value.startswith("//")


class StarFieldsMixin(serializers.Serializer):
    """Field hasil perhitungan untuk model yang punya relasi starred_by."""

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())


class AchievementsSerializer(StarFieldsMixin, serializers.ModelSerializer):
    # Sama seperti AchievementsForm: tulis data wajib menyertakan kode rahasia.
    secret_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Achievements
        fields = [
            "id", "title", "period", "description", "category",
            "achievements_image_url",
            "star_count", "is_starred", "starred_by_names",
            "secret_code",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama penghargaan tidak boleh hanya berisi tag HTML.")
        return value

    def validate_period(self, value):
        return strip_tags(value or "").strip()

    def validate_description(self, value):
        return strip_tags(value).strip()

    def validate(self, attrs):
        # secret_code bukan field model, jadi dibuang setelah diperiksa.
        code = attrs.pop("secret_code", None)
        expected = os.getenv("PORTOFOLIO_SECRET")
        if not code or not expected or not secrets.compare_digest(code, expected):
            raise serializers.ValidationError(
                {"secret_code": ["Kode rahasia yang anda masukkan salah."]}
            )
        return attrs


class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    category_display = serializers.CharField(source="get_category_display", read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "title", "institution", "period", "category", "category_display",
            "description", "logo", "website",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama experience tidak boleh kosong.")
        return value

    def validate_institution(self, value):
        return strip_tags(value or "").strip()

    def validate_period(self, value):
        return strip_tags(value or "").strip()

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Deskripsi experience tidak boleh kosong.")
        return value

    def validate_logo(self, value):
        value = strip_tags(value or "").strip()
        if not _is_safe_url(value, allow_relative=True):
            raise serializers.ValidationError("Logo harus berupa path /static/... atau URL http(s).")
        return value

    def validate_website(self, value):
        value = strip_tags(value or "").strip()
        if not _is_safe_url(value):
            raise serializers.ValidationError("Website harus berupa URL http(s).")
        return value
