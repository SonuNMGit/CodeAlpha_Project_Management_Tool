from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User 
from django.db import IntegrityError 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, ProjectForm
from .models import Task, Comment, TaskLink, Project, UserProfile
from django.http import HttpResponseForbidden

def home(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_profile = UserProfile.objects.get(user=user)
            login(request, user)
            if user_profile.role == 'manager':
                return redirect('manager_home')  
            else:
                return redirect('team_member_home') 
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')

        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user_profile = UserProfile(user=user, role=role)
                user_profile.save()
                login(request, user)
                return redirect('login')  
            except IntegrityError:
                messages.error(request, "Username already taken.")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'signup.html')

from .forms import  PasswordResetForm

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print("Attempting to reset password for user:", username)
            try:
                user = User.objects.get(username=username)
                new_password = form.cleaned_data['new_password1']
                user.set_password(new_password)
                user.save()
                print("Password updated successfully.")  
                return redirect('login') 
            except User.DoesNotExist:
                form.add_error(None, "User does not exist.")
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

@login_required
def team_member_home(request):
    user = request.user
    user_projects = Project.objects.filter(team_members=user)
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
            'user_projects': user_projects,
            'user_profile': user_profile,  
        }
    return render(request, 'team_member_home.html',context)

@login_required
def manager_home(request):
    user_projects = Project.objects.filter(creator=request.user) 
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
            'user_projects': user_projects,
            'user_profile': user_profile,  
        }
    return render(request, 'manager_home.html',context)

@login_required
def create_project(request):
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user  
            project.save()
           
            team_member_ids = request.POST.getlist('team_members')
            project.team_members.set(team_member_ids)
            return redirect('manager_home')  
    else:
        form = ProjectForm()

    team_members = UserProfile.objects.filter(role='team_member').select_related('user')
    
    return render(request, 'create_project.html', {
        'form': form,
        'team_members': team_members,
        'user_profile': user_profile,
    })

@login_required
def edit_project(request, project_id):
    user_profile = UserProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            team_member_ids = request.POST.getlist('team_members')
            project.team_members.set(team_member_ids)
            return redirect('manager_home')  
    else:
        form = ProjectForm(instance=project)
    
    team_members = UserProfile.objects.filter(role='team_member').select_related('user')
      
    context = {
            'form': form,
            'user_profile': user_profile,
            'team_members': team_members,
        }
    return render(request, 'edit_project.html', context)

@login_required
def delete_project(request, project_id):
    user_profile = UserProfile.objects.get(user=request.user)
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('manager_home') 
    context = {
            'project': project,
            'user_profile': user_profile,  
        }
    return render(request, 'confirm_delete.html', context)

@login_required
def assign_task(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project 
            task.save()
            return redirect('manager_home')
    else:
        form = TaskForm(project=project)

    return render(request, 'assign_task.html', {'form': form, 'project': project,'user_profile': user_profile})

@login_required
def task_edit(request, task_id):
    user_profile = UserProfile.objects.get(user=request.user)
    task = get_object_or_404(Task, id=task_id)
    project = task.project  
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, project=project) 
        if form.is_valid():
            form.save()
            return redirect('manager_home')
    else:
        form = TaskForm(instance=task, project=project) 

    return render(request, 'edit_task.html', {'form': form, 'task': task,'user_profile': user_profile})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id) 

    if request.method == 'POST':
        task.delete()  
        return redirect('manager_home') 

    return render(request, 'manager_home.html', {'task': task}) 

@login_required
def save_task_link(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.assigned_to == request.user and request.method == 'POST':
        link = request.POST.get('link')
        TaskLink.objects.create(task=task, link=link)
        return redirect('team_member_home') 

    return redirect('team_member_home')

@login_required
def delete_task_link(request, link_id):
    task_link = get_object_or_404(TaskLink, id=link_id)

    if task_link.task.assigned_to == request.user:
        task_link.delete()  
    return redirect('team_member_home')  

@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(task=task, user=request.user, content=content)
    return redirect(request.META.get('HTTP_REFERER')) 

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER')) 
    else:
        return HttpResponseForbidden('You are not allowed to delete this comment.')
