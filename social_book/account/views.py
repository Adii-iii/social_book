from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request, "account\\index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken")
            return redirect("signup")
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname

        myuser.save()

        messages.success(request, "Account successfully created")
        return redirect("signin")

    return render(request, "account\\register.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")
        print(username, password)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name  # type: ignore
            print(fname, "logged in")
            return render(request, "account\\index.html", {"fname": fname})

        else:
            messages.error(request, "Details are incorrect")
            print("no")
            return redirect("signin")
    return render(request, "account\\login.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")
