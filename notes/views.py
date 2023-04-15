from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def notelist(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    user = request.user
    notes = Note.objects.filter(user = user)
     
    context = {
        'user': user,
        'notes': notes
    }
    return render(request,'notelist.html', context)
def addNote(request):
    user = request.user
    if request.method == "POST":
        form = request.POST
        note = Note(body = form["body"], user=user)
        note.save()

    return render(request,'addNote.html')
def noteDetail(request, id):
    user = request.user
    note = Note.objects.get(id=id)
    context = {
        'user': user,
        'note': note
    }
    if request.method == "POST":
        form = request.POST
        note.body = form['body']
        note.save()

    return render(request, 'noteDetail.html', context)
def deleteNote(request, id):
    user = request.user
    note = Note.objects.get(id=id)
    note.delete()

    return HttpResponseRedirect(reverse('notelist'))
def Login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = request.POST
            user = authenticate(username = form['username'],password = form['password'] )
            if user is not None:
                login(request,user)
            else:
                return render(request, 'login.html')
    else:
        return HttpResponseRedirect(reverse('notelist'))
def Logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))