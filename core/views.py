import os
import zipfile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import UploadForm
from .models import ProjectUpload

# -------------------------------
# Home Page (no login required)
# -------------------------------
def home(request):
    return render(request, "home.html")


# -------------------------------
# Upload Project (requires login)
# -------------------------------
@login_required
def upload_project(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save uploaded file linked to user
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            # Extract ZIP file
            file_path = project.uploaded_file.path
            extract_dir = os.path.join(settings.BASE_DIR, "media", "extracted", str(project.id))
            os.makedirs(extract_dir, exist_ok=True)

            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_dir)
                project.extracted_path = extract_dir
                project.save()
            except zipfile.BadZipFile:
                # Handle invalid ZIP
                project.delete()
                return render(request, "upload.html", {
                    "form": form,
                    "error": "Uploaded file is not a valid ZIP."
                })

            # Redirect to docs view
            return redirect("view_docs", project_id=project.id)
    else:
        form = UploadForm()

    return render(request, "upload.html", {"form": form})


# -------------------------------
# View Generated Docs (requires login)
# -------------------------------
@login_required
def view_docs(request, project_id):
    project = get_object_or_404(ProjectUpload, id=project_id, user=request.user)

    return render(request, "docs_generated.html", {
        "project": project
    })
