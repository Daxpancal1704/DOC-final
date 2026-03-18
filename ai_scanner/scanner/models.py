from django.db import models
from django.contrib.auth.models import User


class DocumentUpload(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ImageUpload(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name

class TextInput(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

class ScanHistory(models.Model):
        SCAN_TYPES = (
            ("document", "Document"),
            ("image", "Image"),
            ("text", "Text"),
        )

        user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

        scan_type = models.CharField(max_length=20, choices=SCAN_TYPES)

        file_name = models.CharField(max_length=255, blank=True)

        result = models.CharField(max_length=100)

        accuracy = models.FloatField()

        details = models.TextField(blank=True)

        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"{self.scan_type} - {self.result}"