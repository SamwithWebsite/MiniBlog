from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import User_SignupForm,LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from .forms import postForm
from django.contrib.auth.models import Group

# Create your views here.
def homes(request):
    posts = Post.objects.all()
    return render(request,'home.html',{'Posts':posts})

def about(request):
    return render(request,'about.html')


def contact(request):
    return render(request,'contact.html')

def dashbord(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()

        return render(request,'dashbord.html',{'posts':posts})
    else:
       return HttpResponseRedirect('/login/')

def user_logout(request):
     logout(request)
     return HttpResponseRedirect('/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in Successfully')
                    return HttpResponseRedirect('/dashbord/')
        else:
            form = LoginForm()
        return render(request,'login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashbord/')

def user_signup(request):
    if request.method == 'POST':
        form = User_SignupForm(request.POST)

        if form.is_valid():
            messages.success(request,'Successfully created Accout')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)   
    else:
        form = User_SignupForm()
    return render(request,'sign.html',{'form':form})

def addpost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = postForm(request.POST)

            if form.is_valid():
                form.save()
                form = postForm()
        else:
            form = postForm()
        return render(request,'addpost.html',{'form':form})
    else:
        return HttpResponse('<h1>Error 404</h>')

def update_post(request,id):
    if request.user.is_authenticated: 
        if request.method =='POST':
            pi = Post.objects.get(pk=id)
            form = postForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = postForm(instance=pi)
        return render(request,'update.html',{'form':form})

    else:
        return HttpResponseRedirect('/login/')
    

def delete_post(request,id):
    if request.user.is_authenticated: 
        if request.method =='POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashbord/') 
    else:
        return HttpResponseRedirect('/login/')
    