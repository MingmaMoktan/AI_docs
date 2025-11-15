from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_project, name='upload_project'),
    path('docs/<int:project_id>/', views.view_docs, name='view_docs'),
]
