from django.shortcuts import render
from django.db.models import Avg
from register.models import Project
from projects.models import Task
from projects.forms import TaskRegistrationForm
from projects.forms import ProjectRegistrationForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def projects(request):
    user = request.user
    tasks = Task.objects.filter(assign=user)
    projects = Project.objects.filter(task__in=tasks).distinct()
    for project in projects:
        total_tasks = project.task_set.count()
        completed_tasks = project.task_set.filter(status='5').count()
        project.completion_percentage = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    total_tasks = tasks.count()
    completed_tasks = Task.objects.filter(status='5').count()
    avg_projects = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    

    overdue_tasks = tasks.filter(due='2')
    context = {
        'avg_projects' : avg_projects,
        'projects' : projects,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
    }
    return render(request, 'projects/projects.html', context)

def projectDetails(request, slug):
    project = get_object_or_404(Project, slug=slug)
    tasks = Task.objects.filter(project=project)
    total_tasks = tasks.count()
    completed_tasks = Task.objects.filter(project=project, status='5').count()
    
    percentage_complete = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    context = {
        'project' : project,
        "tasks": tasks,
        'total_tasks' : total_tasks,
        'completed_tasks' : completed_tasks,
        'percentage_complete' : percentage_complete
        
    }
    return render(request, 'projects/project_details.html', context)

@login_required
def Tasks(request):
    user = request.user
    projects = Project.objects.all()
    tasks = Task.objects.filter(assign=user).exclude(status='5')
    overdue_tasks = tasks.filter(due='2')
    context = {
        'projects' : projects,
        'tasks' : tasks,
        'overdue_tasks' : overdue_tasks,
    }
    return render(request, 'projects/my_tasks.html', context)
@login_required
def ApprovedTasks(request):
    user = request.user
    projects = Project.objects.all()
    tasks = Task.objects.filter(assign=user, status="5")
 
    context = {
        'projects' : projects,
        'tasks' : tasks,
  
    }
    return render(request, 'projects/approved_tasks.html', context)

def newTask(request):
    if request.method == 'POST':
        form = TaskRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_task.html', context)
        else:
            return render(request, 'projects/new_task.html', context)
    else:
        form = TaskRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'projects/new_task.html', context)

def newProject(request):
    if request.method == 'POST':
        form = ProjectRegistrationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            form.save()
            created = True
            form = ProjectRegistrationForm()
            context = {
                'created': created,
                'form': form,
            }
            return render(request, 'projects/new_project.html', context)
        else:
            return render(request, 'projects/new_project.html', context)
    else:
        form = ProjectRegistrationForm()
        context = {
            'form': form,
        }
        return render(request,'projects/new_project.html', context)
    
def update_task_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        task.status = new_status
        task.save()
    return redirect('projects:my-tasks')


def update_task_due(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        new_due = request.POST.get('due')
        task.due = new_due
        task.save()
    return redirect('projects:my-tasks')