from django import forms
from .models import ProjectUpload

class UploadForm(forms.ModelForm):
    class Meta:
        model = ProjectUpload
        fields = ["uploaded_file"]
