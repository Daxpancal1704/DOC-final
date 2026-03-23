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
    
    def clean_file(self):

        file = self.cleaned_data.get('file')

        allowed_extensions = ['pdf', 'docx', 'txt']

        file_name = file.name.lower()
        extension = file_name.split('.')[-1]

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only PDF, DOCX, and TXT files are allowed. Images are not supported."
            )

        return file    


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']
        
    def clean_image(self):

        image = self.cleaned_data.get('image')

        allowed_extensions = ['jpg', 'jpeg', 'png']

        file_name = image.name.lower()
        extension = file_name.split('.')[-1]

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only JPG, JPEG, and PNG images are allowed. Documents are not supported."
            )

        return image

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