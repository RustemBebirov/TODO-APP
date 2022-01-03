from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import TaskForm, ShareFriendForm
from .models import Task, Friends, TaskComment
from trash.models import Trash

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required(login_url="login")
def home(request):
    tasks = Task.objects.filter(user=request.user,done=False).all()
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user_id = request.user.id
            task.save()
            messages.success(request,'Task elave olundu')
            return redirect('home')
        else:
            messages.warning(request,'Task elave olunmadi')
    context = {
        'form':form,
        'tasks':tasks
    }   

    return render(request,'index.html',context)

@login_required(login_url="login")
def detail(request,pk):
    task = Task.objects.filter(pk=pk).first()
    friend = Friends.objects.filter(task=task).first()
    if friend:
        if request.user != friend.friend:
            raise PermissionDenied
    else:
        if request.user != task.user:
            raise PermissionDenied
    comments = TaskComment.objects.filter(task=task)
    return render(request,'detail.html',{'task':task,'comments':comments})


@login_required(login_url="login")
def update_task(request,pk):
    task = Task.objects.filter(pk=pk).first()
    form = TaskForm(instance=task)
    friend = Friends.objects.filter(task=task).first()
    if friend:
        if request.user != friend.friend or friend.is_edit == False:
            raise PermissionDenied
    else:
        if request.user != task.user:
            raise PermissionDenied
    if request.method == 'POST':
        form = TaskForm(data=request.POST,instance=task)
        if form.is_valid():
            form.save()
            messages.success(request,'Task update olundu')
            return redirect('home')
        else:
            messages.warning(request,'Task update olunmadi')


    context= {
        'form':form
    }

    return render(request,'update.html',context)

@login_required(login_url="login")
def delete_task(request,pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user != request.user:
        raise PermissionDenied
    trash = Trash.objects.create(task=task,user=request.user)
    messages.success(request,'Task zibil qutusuna elave olundu')
    return redirect('home')

@login_required(login_url="login")
def privacy_task(request,pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user != request.user:
        raise PermissionDenied
    if task.privacy == True:
        task.privacy = False
        task.save()
        messages.warning(request,'Task gizledildi')
    else:
        task.privacy = True
        task.save()
        messages.success(request,'Task gorsenir')
    return redirect('home')


@login_required(login_url="login")
def history(request):
    tasks = Task.objects.filter(user=request.user,done=True).all()

    return render(request,'history.html',{'tasks':tasks})


@login_required(login_url="login")
def share_task(request,pk):
    task = Task.objects.filter(pk=pk).first()
    if task.user != request.user:
        raise PermissionDenied  
    form = ShareFriendForm()
    shared_tasks = Friends.objects.filter(task=task).all()
    if request.method == 'POST':
        form = ShareFriendForm(data=request.POST)
        user_email = request.POST.get('email')
        user = User.objects.filter(email=user_email).first() 
        if form.is_valid():
            if user:
                check_friend = Friends.objects.filter(friend=user,task=task).first()
                print(check_friend)
                if check_friend:
                    messages.warning(request,'Taski artiq paylasmisiniz')
                else:
                    
                        friend = form.save(commit=False)
                        friend.friend = user
                        friend.task = task
                        friend.save()
                        messages.success(request,'Dostunuzla paylasildi')
                        return redirect('share_task',pk)
            else:
                messages.warning(request,'Bu emailde istifadeci yoxdu')
                return redirect('share_task',pk)

    context = {
        'form':form,
        'task':task,
        'shared_tasks':shared_tasks,
    }
    return render(request,'share.html',context)


@login_required(login_url="login")
def shared_task_list(request):
    shared_task_lists = Friends.objects.filter(friend=request.user).all()

    context = {
        'shared_task_lists': shared_task_lists
    }
    return render(request,'shared_tasks.html',context)


@login_required(login_url="login")
def delete_friend(request,pk):
    friend = Friends.objects.filter(pk=pk).first()
    friend.delete()
    messages.success(request,'Dostunuz silindi')
    return redirect('share_task',pk)