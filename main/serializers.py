import os
import secrets

from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Achievements, Education, Experience


def _is_safe_url(value, allow_relative=False):
    """URL kosong, http(s), atau (opsional) path relatif seperti /static/img/a.png."""
    # Note: ini buat nolak skema berbahaya kayak javascript:alert(1) di field logo/website/gambar.
    # "//" dilarang juga karena itu bisa dianggap browser sebagai URL ke domain lain.
    if not value:
        return True
    if value.startswith(("http://", "https://")):
        return True
    return allow_relative and value.startswith("/") and not value.startswith("//")


class StarFieldsMixin(serializers.Serializer):
    """
    Field hasil perhitungan untuk model yang punya relasi starred_by.
    Ketiganya SerializerMethodField, jadi otomatis read-only: kalau client nekat kirim
    star_count=99 lewat POST/PUT, nilainya diabaikan dan tetap dihitung dari database.
    Dibuat sebagai mixin biar ga ditulis ulang di tiga serializer.
    """

    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        # request diambil dari context yang dikirim view; user yang belum login selalu False
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        # cuma username yang dikeluarkan, jadi data sensitif user (email, password) tidak ikut bocor
        return ", ".join(user.username for user in obj.starred_by.all())


class AchievementsSerializer(StarFieldsMixin, serializers.ModelSerializer):
    # Sama seperti AchievementsForm: membuat data baru wajib menyertakan kode rahasia.
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

    # validate_<nama_field> dipanggil otomatis oleh DRF untuk tiap field.
    # strip_tags dipakai biar input kayak "<script>..." ga tersimpan ke database (cegah XSS).
    def validate_title(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Nama penghargaan tidak boleh hanya berisi tag HTML.")
        return value

    def validate_period(self, value):
        return strip_tags(value or "").strip()

    def validate_description(self, value):
        value = strip_tags(value).strip()
        if not value:
            raise serializers.ValidationError("Deskripsi penghargaan tidak boleh kosong.")
        return value

    # validate() dipakai untuk aturan yang melibatkan lebih dari satu field / konteks request
    def validate(self, attrs):
        # secret_code bukan kolom model, jadi selalu dibuang dari data yang disimpan.
        code = attrs.pop("secret_code", None)

        # Kode rahasia hanya diwajibkan saat membuat achievement baru (POST).
        # Update (PUT/PATCH) oleh Editor atau pemilik tidak perlu memasukkan ulang kode,
        # sama seperti form edit di halaman Achievements yang menyembunyikan field-nya.
        if self.instance is not None:
            return attrs

        # compare_digest dipakai (bukan ==) supaya perbandingan kodenya aman dari timing attack
        expected = os.getenv("PORTOFOLIO_SECRET")
        if not code or not expected or not secrets.compare_digest(code, expected):
            raise serializers.ValidationError({
                "secret_code": ["Kode rahasia yang anda masukkan salah."]
            })

        return attrs


class ExperienceSerializer(StarFieldsMixin, serializers.ModelSerializer):
    # label kategori yang enak dibaca (mis. "Part-Time"); read_only karena cuma buat tampilan
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

class EducationSerializer(StarFieldsMixin, serializers.ModelSerializer):
    # Education tidak butuh secret_code seperti Achievements, jadi validasinya cuma
    # bersihin tag HTML dan memastikan field wajib tidak kosong.
    class Meta:
        model = Education
        fields = [
            "id",
            "institution",
            "degree",
            "period",
            "logo",
            "website",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]
        # field hasil perhitungan ditulis eksplisit di sini juga biar jelas kalau ini tidak bisa diisi client
        read_only_fields = [
            "id",
            "star_count",
            "is_starred",
            "starred_by_names",
        ]

    def validate_institution(self, value):
        value = strip_tags(value or "").strip()
        if not value:
            raise serializers.ValidationError("Nama institusi pendidikan tidak boleh kosong.")
        return value

    def validate_degree(self, value):
        value = strip_tags(value or "").strip()
        if not value:
            raise serializers.ValidationError("Gelar atau jurusan pendidikan tidak boleh kosong.")
        return value

    def validate_period(self, value):
        return strip_tags(value or "").strip()

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
