import uuid #impor library uuid untuk buat id unik secara otomatis
from django.db import models #impor models django untuk membuat model dan field database

# ----->>>>> MODEL EXPERIENCE <<<<<-----
class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    #id utama dengan uuid agar tiap data punya identifier unik
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # simpan judul maks 255 karakter
    title = models.CharField(max_length=255)

    # simpan institusi boleh kosong (optional) krn kalau blank=True dan null= True
    institution=models.CharField(max_length=100,blank=True, null=True)

    # simpan deskripsi
    description = models.TextField()

    # simpan kategori dari yg sudah ditentukan di atas "EXPERIENCE_CHOICES" 
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')

    # Note: untuk thumbnail started_at dan ended_at saya ga pakai saya ganti dengan period logo dan website
        # thumbnail = models.URLField(blank=True, null=True)
        # started_at = models.DateTimeField(auto_now_add=True)
        # ended_at = models.DateTimeField(blank=True, null=True)
    #periode pengalaman maks 50 karakter boleh kosong (optional) krn kalau blank=True dan null= True
    period = models.CharField(max_length=50, blank=True, null=True)

    #logo pengalaman maks 255 karakter boleh kosong (optional) krn kalau blank=True dan null= True
    logo = models.CharField(max_length=255, blank=True, null=True)

    #website pengalaman maks 255 karakter boleh kosong (optional) krn kalau blank=True dan null= True
    website = models.CharField(max_length=255, blank=True, null=True)

    # Menentukan representasi object Experience ketika object tersebut ditampilkan sebagai string.
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
# ----->>>>> MODEL EDUCATION <<<<<-----
# Note: saya membagi beberapa kategori dlm bagian yg saya gunakan sebelumnya di tugas 1
class Education(models.Model):
    # simpan institusi pensiiskan
    institution=models.CharField(max_length=100)

    # simpan jurusan
    degree=models.CharField(max_length=100)

    # simpan periode
    period= models.CharField(max_length=50)

    # simpan logo institusi
    logo =models.CharField(max_length=50)
    
    # simpan website
    website= models.CharField(max_length=100)

    # Menentukan representasi object Education
    # ketika object tersebut ditampilkan sebagai string.
    def __str__(self):
        return self.institution