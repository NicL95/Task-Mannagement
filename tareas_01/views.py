from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# from django.http import HttpResponse
from django.db import IntegrityError
from .forms import formTareas
from .models import Tareas
from django.utils import timezone


# Create your views here.

def inicio(request):
    return render(request, 'inicio.html', {
    })


def register(request):
    if request.method == 'GET':
        return render(request, 'registrarse.html', {
            'formulario': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                usuario = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                usuario.save()
                login(request, usuario)
                return redirect('tareas')
            except IntegrityError:
                return render(request, 'registrarse.html', {
                    'formulario': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'registrarse.html', {
            'formulario': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })


def iniciarSesion(request):
    if request.method == 'GET':
        return render(request, 'iniciarSesion.html', {
            'iniciar': AuthenticationForm
        })
    else:
        usuario = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if usuario is None:
            return render(request, 'iniciarSesion.html', {
                'iniciar': AuthenticationForm,
                'error': 'Usuario o Contraseña es incorrecto'
            })
        login(request, usuario)
        return redirect('tareas')


def cerrarSesion(request):
    logout(request)
    return redirect('inicio')


def tareas(request):
    # listaTareas = Tareas.objects.filter(usuario = request.user, fechaCompletada__isnull=True)
    listaTareas = Tareas.objects.filter(fechaCompletada__isnull=True)
    # listaTareas = Tareas.objects.all() #Son todas las tareas para todos los usuarios
    return render(request, 'tareas.html', {
        'listaTareas': listaTareas
    })


def crearTarea(request):
    if request.method == 'GET':
        return render(request, 'crearTarea.html', {
            'formulario': formTareas
        })
    else:
        try:
            formulario = formTareas(request.POST)
            nueva_tarea = formulario.save(commit=False)
            nueva_tarea.usuario = request.user
            nueva_tarea.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'crearTarea.html', {
                'formulario': formTareas,
                'error': 'Error al cargar la tarea: ingrese datos validos'
            })


def detallesTarea(request, idTarea):
    if request.method == 'GET':
        tarea = get_object_or_404(Tareas, pk=idTarea)
        formulario = formTareas(instance=tarea)
        return render(request, 'detallesTarea.html', {
            'tarea': tarea,
            'formulario': formulario
        })
    else:
        try:
            tarea = get_object_or_404(Tareas, pk=idTarea)
            formulario = formTareas(request.POST, instance=tarea)
            formulario.save()
            return redirect('tareas')
        except ValueError:
            return render(request, 'detallesTarea.html', {
                'tarea': tarea,
                'formulario': formulario,
                'error': 'Error al actualizar la tarea'
            })

def completarTarea(request, idTarea):
    tarea = get_object_or_404(Tareas, pk=idTarea)
    if request.method == 'POST':
        tarea.fechaCompletada = timezone.now()
        tarea.save()
        return redirect('tareas')