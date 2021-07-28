from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from .models import MyUser

# Create your views here.
from .forms import RegisterForm


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
                # user.is_staff = True
            except:
                user = None
            if user is not None:
                login(request, user)
                return redirect("/")
    return render(request, "account/register.html", {"form": form})
