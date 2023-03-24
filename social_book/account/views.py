import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView

# from social_book.account import models
from .models import CustomUser, Book, Person, BookUpload
from .forms import BookForm
from django.conf import settings

from rest_framework import views, status
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from .models import UploadedFile
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
# Create your views here.

User = CustomUser


def home(request):
    return render(request, "account\\index.html")


def signup(request):
    if request.method == "POST":
        # username = request.POST["username"]

        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        """if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken")
            return redirect("signup")
            """
        """myuser = User.objects.create_user(username, email, pass1)"""

        if User.objects.filter(email=email).first():
            messages.error(request, "This email is already taken")
            return redirect("signup")
        myuser = User.objects.create_user(email, pass1)
        myuser.first_name = fname

        myuser.save()

        messages.success(request, "Account successfully created")
        return redirect("signin")

    return render(request, "account\\register.html")


def signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass1")
        print(email, password)
        user = authenticate(email=email, password=password)

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


def show(request):
    data = CustomUser.objects.filter(public_visibility=True).values()
    context = {
        "authors": data,
    }
    # print('hello')
    # print(context, "hi")
    return render(request, "account\\authors.html", context)


def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("home")

def upload_book(request):
    if request.method == "POST":
        book = Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            url=request.POST['url'],
        )
        upload = BookUpload.objects.create(
            user=request.user,
            book=book,
            file=request.FILES['file'],
        )
        token = upload.generate_token()
        return render(request, "account/file_token.html", {"token": token, "file_url": upload.file.url})
    else:
        return render(request, "account/upload_book.html")


def view_books(request):
    books = Book.objects.all()
    for book in books:
        book.url = settings.MEDIA_URL + book.file_path
    return render(request, "account//book.html", {"books": books})

@csrf_exempt
@api_view(["GET"])
def person_list(request):
    persons = list(Person.objects.values())
    return JsonResponse(persons, safe=False)
    
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class FileTokenView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, file_id):
        file = get_object_or_404(UploadedFile, pk=file_id)
        if file.user != request.user:
            return Response(status=403)
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({'token': token.key, 'file_url': file.file.url})
    
@csrf_exempt
@api_view(["GET"])
def sample_api(request):
    data = {'sample_data': 123}
    return Response(data, status=status.HTTP_200_OK)