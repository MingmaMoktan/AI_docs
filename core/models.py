from django.db import models
from django.contrib.auth.models import User
import uuid
import os

# Function to generate upload path with user ID and UUID
def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('uploads', str(instance.user.id), filename)

class ProjectUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to=upload_path)  # use custom path with UUID
    extracted_path = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Upload {self.id} by {self.user.username}"

class GeneratedDoc(models.Model):
    project = models.ForeignKey(ProjectUpload, on_delete=models.CASCADE, related_name='docs')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Docs for Project {self.project.id}"
