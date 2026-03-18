from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DocumentUpload, ImageUpload, TextInput



class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ['file']


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


class TextInputForm(forms.ModelForm):

    class Meta:

        model = TextInput

        fields = ["text"]

        widgets = {
            "text": forms.Textarea(attrs={
                "class":"form-control",
                "rows":10,
                "maxlength":5000
            })
        }