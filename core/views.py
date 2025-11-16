import os
import zipfile
from urllib.parse import unquote
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import UploadForm
from .models import ProjectUpload
from .utils import build_file_tree, safe_read_file
from .utils import parse_and_generate_docs  # If you already have this


# ---------------------------
# HOME
# ---------------------------
def home(request):
    return render(request, "home.html")


# ---------------------------
# UPLOAD PROJECT
# ---------------------------
@login_required
def upload_project(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()

            # Extract zip
            file_path = project.uploaded_file.path
            extract_dir = os.path.join(settings.BASE_DIR, "media", "extracted", str(project.id))
            os.makedirs(extract_dir, exist_ok=True)

            try:
                with zipfile.ZipFile(file_path, "r") as z:
                    z.extractall(extract_dir)

                project.extracted_path = extract_dir
                project.save()

                # Parse → generate docs
                parse_and_generate_docs(project)

            except zipfile.BadZipFile:
                project.delete()
                return render(request, "upload.html", {
                    "form": form,
                    "error": "Invalid ZIP file"
                })

            return redirect("file_browser", project_id=project.id)

    else:
        form = UploadForm()

    return render(request, "upload.html", {"form": form})


# ---------------------------
# VIEW PARSED DOCS
# ---------------------------
@login_required
def view_docs(request, project_id):
    project = get_object_or_404(ProjectUpload, id=project_id, user=request.user)

    return render(request, "docs_generated.html", {
        "project": project,
        "docs": project.docs.all()
    })


# ---------------------------
# FILE TREE BROWSER
# ---------------------------
@login_required
def file_browser(request, project_id):
    project = get_object_or_404(ProjectUpload, id=project_id, user=request.user)

    if not project.extracted_path or not os.path.exists(project.extracted_path):
        return render(request, "file_browser.html", {
            "project": project,
            "tree": [],
            "error": "No extracted files found."
        })

    tree = build_file_tree(project.extracted_path)

    return render(request, "file_browser.html", {
        "project": project,
        "tree": tree
    })


# ---------------------------
# FILE VIEWER
# ---------------------------
@login_required
def file_view(request, project_id):
    project = get_object_or_404(ProjectUpload, id=project_id, user=request.user)

    rel_path = request.GET.get("path", "")
    if not rel_path:
        return redirect("file_browser", project_id=project.id)

    rel_path = unquote(rel_path)

    try:
        content, mime = safe_read_file(project.extracted_path, rel_path)
    except Exception as e:
        return render(request, "file_view.html", {
            "project": project,
            "path": rel_path,
            "error": str(e)
        })

    return render(request, "file_view.html", {
        "project": project,
        "path": rel_path,
        "content": content,
        "mime": mime
    })
