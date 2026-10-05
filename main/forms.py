from django import forms
from .models import Achievements,Experience
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "institution",
            "period",
            "category",
            "description",
            "logo",
            "website",
        ]

        labels = {
            "title": "Nama Experience",
            "institution": "Institusi",
            "period": "Periode",
            "category": "Kategori",
            "description": "Deskripsi",
            "logo": "URL Logo",
            "website": "Website",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Nama experience",
                    "maxlength": 255,
                }
            ),
            "institution": forms.TextInput(
                attrs={
                    "placeholder": "Nama institusi",
                    "maxlength": 100,
                }
            ),
            "period": forms.TextInput(
                attrs={
                    "placeholder": "Contoh: 2024 - 2025",
                    "maxlength": 50,
                }
            ),
            "category": forms.Select(),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Ceritakan pengalamanmu",
                    "rows": 4,
                }
            ),
            "logo": forms.TextInput(
                attrs={
                    "placeholder": "/static/img/logo.png",
                    "maxlength": 255,
                }
            ),
            "website": forms.URLInput(
                attrs={
                    "placeholder": "https://example.com",
                }
            ),
        }

    def clean_title(self):
        title = strip_tags(
            self.cleaned_data["title"]
        ).strip()

        if not title:
            raise ValidationError(
                "Nama experience tidak boleh kosong."
            )

        return title

    def clean_institution(self):
        institution = self.cleaned_data.get("institution")

        return strip_tags(
            institution or ""
        ).strip()

    def clean_period(self):
        period = self.cleaned_data.get("period")

        return strip_tags(
            period or ""
        ).strip()

    def clean_description(self):
        description = strip_tags(
            self.cleaned_data["description"]
        ).strip()

        if not description:
            raise ValidationError(
                "Deskripsi experience tidak boleh kosong."
            )

        return description

    def clean_logo(self):
        logo = self.cleaned_data.get("logo")

        return strip_tags(
            logo or ""
        ).strip()
    
class AchievementsForm(forms.ModelForm):
    secret_code=forms.CharField(label="Secret Code", widget=forms.PasswordInput(attrs={"placeholder": "Masukkan kode rahasia anda..."}))
    class Meta:
        model = Achievements
        fields = [
            'title',
            'period',
            'description',
            'category',
            'achievements_image_url'
        ]

        labels = {
            "title": "Nama Penghargaan",
            "period": "Periode Penghargaan",
            "description": "Deskripsi Penghargaan",
            "category": "Kategori Penghargaan",
            "achievements_image_url": "URL Gambar Penghargaan",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Nama Penghargaan",
                    "maxlength": 255,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Ceritakan Penghargaanmu",
                    "rows": 3,
                }
            ),
            "category": forms.Select(),
            "period": forms.TextInput(
                attrs={
                    "placeholder":  "Masukkan periode penghargaan",
                    }
            ),
            "achievements_image_url": forms.URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),

        }

    def clean_title(self):
        title = strip_tags(self.cleaned_data["title"]).strip()
        if not title:
            raise ValidationError(
                "Nama penghargaan tidak boleh hanya berisi tag HTML."
            )
        return title

    def clean_period(self):
        return strip_tags(self.cleaned_data["period"]).strip()

    def clean_description(self):
        return strip_tags(self.cleaned_data["description"]).strip()