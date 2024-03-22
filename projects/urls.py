from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<slug:slug>/', views.projectDetails, name='project_details'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    path('my-tasks/', views.Tasks, name='my-tasks'),
    path('approved-tasks/', views.ApprovedTasks, name='approved-tasks'),
    path('update_task_status/<int:task_id>/', views.update_task_status, name='update_task_status'),
    path('update_task_due/<int:task_id>/', views.update_task_due, name='update_task_due'),
]