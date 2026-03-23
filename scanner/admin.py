from django.contrib import admin
from .models import DocumentUpload, ImageUpload, TextInput,ScanHistory


admin.site.register(DocumentUpload)
admin.site.register(ImageUpload)
admin.site.register(TextInput)
admin.site.register(ScanHistory)