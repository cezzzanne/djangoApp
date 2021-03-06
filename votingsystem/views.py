from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CreateProfileForm, EditProfileForm, FolderForm, AddToDoForm
from django.contrib.auth import update_session_auth_hash
from .models import Folder, ToDo
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        user = CreateProfileForm(request.POST)
        if user.is_valid():
            user.save()
            return HttpResponseRedirect('/login')
    return render(request, 'registration/register.html', {'form': CreateProfileForm})


def home(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/account/home')

    return render(request, 'home.html')


@login_required()
def login_home(request):
    original_form = FolderForm
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            add = Folder(user=request.user.profile, name=name, description=description)
            add.save()
            return HttpResponseRedirect('/account/home')

    return render(request, 'registration/login_home.html', {'form': original_form})


@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/account/home')
    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'registration/edit_profile.html', {'form': form})


@login_required()
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect('/account/home')
        else:
            return HttpResponseRedirect('/account/edit-password')
    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'registration/edit_password.html', {'form': form})


@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@login_required()
def add_todo(request, folder):
    add_todo_form = AddToDoForm
    folder_object = Folder.objects.get(id=folder)
    todos = ToDo.objects.filter(folder=folder_object)
    if request.method == 'POST':
        complete_form = AddToDoForm(data=request.POST)
        if complete_form.is_valid():
            name = complete_form.cleaned_data['name']
            note = complete_form.cleaned_data['note']
            todo = ToDo(folder=folder_object, name=name, note=note)
            todo.save()
            return render(request, 'registration/add_todo.html', {'form': add_todo_form, 'todos': todos})

    else:
        return render(request, 'registration/add_todo.html', {'form': add_todo_form, 'todos': todos})


@login_required()
def add_folder(request):
    original_form = FolderForm
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            add = Folder(user=request.user.profile, name=name, description=description)
            add.save()
            return HttpResponseRedirect('/account/home')
    else:
        return render(request, 'registration/add_folder.html', {'form': original_form})


@login_required
def delete_todo(request, todo):
    todo_object = ToDo.objects.get(id=todo)
    todo_object.delete()
    return HttpResponseRedirect('/account/home')
