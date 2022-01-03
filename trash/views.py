from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Trash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import Task

@login_required(login_url="login")
def trash_list(request):
    trash_lists = Trash.objects.filter(user=request.user).all()

    context = {
        'trash_lists':trash_lists
    }
    return render(request,'trash.html',context)


@login_required(login_url="login")
def done_task(request,pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user != request.user:
        raise PermissionDenied
    if request.method == 'POST':        
        options = request.POST.get('options')
        if options == "False": 
            task.done = True
            task.save()
            messages.success(request,'Task yerine yetirildi')
        else:        
            task.done = False
            task.save()
            messages.warning(request,'Task yerine yetirilmedi')
  
    return redirect('home')



@login_required(login_url="login")
def save_task(request,pk):
    trash_task = Trash.objects.filter(pk=pk).first()
    if trash_task.user != request.user:
        raise PermissionDenied
    trash_task.delete()

    messages.success(request,'Task zibil qutusunan cixarildi ')
    return redirect('home')