from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.http import require_POST, require_http_methods
from .forms import CustomUserCreationForm
# Create your views here.


@require_http_methods(['GET','POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('feed:index')
    if request.method=='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)

            return redirect('feed:index')
    
    else: 
        form = CustomUserCreationForm()
    context={
        'form':form,
    }
    return render(request,'account/signup.html',context)


@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('feed:index')

    if request.method =='POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            return redirect(request.GET.get('next') or 'feed:index')
    else:
        form = AuthenticationForm()
    context={
        'form':form,
    }
    return render(request,'account/login.html',context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('feed:index')
    

def profile(request, user_pk):
    person = get_object_or_404(get_user_model(), pk=user_pk)
    context = {
        'person': person,
    }
    return render(request, 'account/profile.html', context)


@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:

        you = get_object_or_404(get_user_model(), pk=user_pk)
        me = request.user

        if me != you:
            if you.followers.filter(pk=me.pk).exists():
                you.followers.remove(me)
            else:
                you.followers.add(me)
        return redirect('account:profile', you.pk)
    else:
        return redirect('account:login')
