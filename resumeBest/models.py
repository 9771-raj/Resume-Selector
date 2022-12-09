from django.db import models

# Create your models here.

class UploadPdf(models.Model):
    jobDescription=models.TextField(max_length=10000)
    resumes = models.FileField(upload_to="")