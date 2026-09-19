from django import forms
from .models import Achievements


class AchievementsForm(forms.ModelForm):
    secret_code=forms.CharField(label="Secret Code", widget=forms.PasswordInput(attrs={"placeholder": "Masukkan kode rahasia anda..."}))
    class Meta:
        model = Achievements
        fields = [
            'title',
            'period',
            'description',
            'category',
            # 'achievements_image_url'
        ]

        labels = {
            "title": "Nama Penghargaan",
            "period": "Periode Penghargaan",
            "description": "Deskripsi Penghargaan",
            "category": "Kategori Penghargaan",
            # "achievements_image_url": "URL Gambar Penghargaan",
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
            # "achievements_image_url": forms.URLInput(
            #     attrs={
            #         "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
            #     }
            # ),

        }