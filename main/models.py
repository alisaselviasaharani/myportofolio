import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

#Class Education
# Note: saya membagi beberapa kategori dlm bagian yg saya gunakan sebelumnya di tugas 1
class Education(models.Model):
    institution=models.CharField(max_length=100)
    degree=models.CharField(max_length=100)
    period= models.CharField(max_length=50)
    logo =models.CharField(max_length=50)
    website= models.CharField(max_length=100)

    def __str__(self):
        return self.institution