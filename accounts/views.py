from django.shortcuts import redirect, render
from .forms import CustomUserChangeForm, CustomUserCreationForm, LoginForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login as django_login, logout as django_logout, authenticate
from django.utils.encoding import force_str
from .tokens import account_activation_token
from .tasks import send_confirmation_mail
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
User = get_user_model()

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    else:

        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(data=request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(username=email, password=password)
                if user:
                    django_login(request,user)
                    messages.success(request,'Siz login oldunuz')
                    return redirect(reverse_lazy('home'))
                else:
                    messages.error(request,'Siz login ola bilmediniz')


        context = {
            'form':form
        }
        return render(request,'login.html',context)


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('home'))
    else:
        form = CustomUserCreationForm()
        if request.method == 'POST':
            form = CustomUserCreationForm(data=request.POST)
            if form.is_valid():
                user = form.save(commit=False) 
                user.is_active = False 
                user.save() 
                site_address = request.is_secure() and "https://" or "http://" + request.META['HTTP_HOST'] 
                send_confirmation_mail(user_id=user.id, site_address=site_address) 
                messages.success(request,'Siz ugurla qeydiyatdan kecdiniz')
                return redirect(reverse_lazy('login'))
        
        context = {
            'form':form,
        }

        return render(request,'register.html',context)


def activate(request, uidb64, token): 

    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) 
        user = User.objects.get(pk=uid) 
    except:
        (TypeError, ValueError, OverflowError, User.DoesNotExist) 
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Email is activated')
        return redirect(reverse_lazy('home'))

    elif user:
        messages.error(request, 'Email is not activated. May be is already activated')
        return redirect(reverse_lazy('register'))

    else:
        messages.error(request, 'Email is not activated')
        return redirect(reverse_lazy('register'))


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
        messages.success(request,'Siz ugurla cixis elediniz')
        return redirect(reverse_lazy('login'))
        
    else:
        return redirect(reverse_lazy('home'))
        