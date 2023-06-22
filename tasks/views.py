from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from django.http import JsonResponse
from .forms import TaskForm
from django.utils import timezone


@login_required
def list_tasks(request):
    """Renders the task list"""
    tasks = Task.objects.all()
    form = TaskForm()
    context = {"tasks": tasks, "form": form}
    return render(request, "tasks/task_list.html", context)


@login_required
def create_task(request):
    """Creates a new task"""
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            task.user = request.user
            task.save()
            print(task.user)
            messages.success(request, "Task created successfully.")
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_list.html', {'form': form})


@login_required
def update_task(request, pk):
    """Updates an exisiting task"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully")
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_list.html', {'form': form})


@login_required
def delete_task(request, pk):
    """Renders the delete task form"""
    form = TaskForm()
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.delete()
    return redirect('tasks')


@login_required
def dashboard(request):
    completed_tasks = request.session.get('completed_tasks', [])
    completed_tasks = [str(task_id) for task_id in completed_tasks]

    user_profile = request.user.userprofile
    xp = user_profile.xp

    task = Task.objects.all()
    completed = 0
    in_progress = 0
    not_started = 0
    due_today = 0

    for t in task:
        if t.due_date == timezone.now().date():
            due_today += 1
        if t.status == "C":
            completed += 1
        if t.status == "IP":
            in_progress += 1
        if t.status == "P":
            not_started += 1

    context = {
        "tasks": task,
        "completed_tasks": completed_tasks,
        "completed": completed,
        "in_progress": in_progress,
        "not_started": not_started,
        "due_today": due_today,
        "xp": xp
        }
    return render(request, "tasks/dashboard.html", context)


@login_required
def mark_completed(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.mark_completed()
    return JsonResponse({'status': 'success'})
