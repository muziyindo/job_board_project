from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings




# Create your views here.
from django.contrib.auth import authenticate, login, logout
from .models import MyUser, Profile

# Create your views here.
from .forms import RegisterForm, LoginForm, ResetPasswordForm


# my_user = MyUser()


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            firstname = form.cleaned_data.get("firstname")
            lastname = form.cleaned_data.get("lastname")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            try:
                user = MyUser.objects.create_user(firstname=firstname, lastname=lastname,
                                                  username=email, email=email,
                                                  password=password)

                user.profile.user_type = form.cleaned_data.get('user_type')
                user.save()

            except:
                user = None
            if user is not None:
                user.is_active = True
                user.is_staff = True
                user.save()
                login(request, user)
                return redirect("/")
    return render(request, "account/register.html", {"form": form, 'page_title': 'New User Registeration'})


def signin(request):
    form = LoginForm(request.POST or None)
    error = ""
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # user is valid and active -> is_active
            # request.user == user
            login(request, user)
            return redirect("/")
        else:
            error = "Invalid username/password"

    return render(request, "account/login.html",
                  {"form": form, "error": error, 'page_title': 'Sign in to your account'})


def signout(request):
    logout(request)
    # request.user == Anon User
    return redirect("/")


def forget_password(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
    return render(request, "account/forget-password.html", {"form": form, 'page_title': 'Reset Your Account Password'})


def forget_password_response(request):
    return render(request, "account/forget-password-response.html")
