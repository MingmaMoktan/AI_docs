from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_project, name="upload_project"),
    path("docs/<int:project_id>/", views.view_docs, name="view_docs"),
    path("projects/<int:project_id>/browser/", views.file_browser, name="file_browser"),
    path("projects/<int:project_id>/file/", views.file_view, name="file_view"),
]
