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
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Account successfully created")
        return redirect("signin")

    return render(request, "account\\register.html")


def signin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("pass1")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name  # type: ignore
            return render(request, "", {'fname': fname})

        else:
            messages.error(request, "Details are incorrect")
            return redirect("home")
    return render(request, "account\\login.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")
