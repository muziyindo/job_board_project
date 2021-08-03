from django import forms
from .models import MyUser
from django.contrib.auth import get_user_model


# non_allowed_usernames = ['abc']
# check for unique email & username

# my_user = MyUser()

USER_TYPE = [
    ('1', 'I am an employer'),
    ('2', 'I am a job seeker'),
]


class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Firstname'}))
    lastname = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Lastname'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        )
    )

    user_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={}), choices=USER_TYPE)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # fetch record from user table and ignore the case
        qs = MyUser.objects.filter(username__iexact=username)
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        qs = MyUser.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")

class LoginForm(forms.Form):
    username = forms.EmailField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "id": "sender-email",
            "placeholder": "Email"
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "user-password",
                "placeholder": "Password"
            }
        )
    )

    def clean(self):
        data = super().clean()
        username = data.get("username")
        password = data.get("password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = MyUser.objects.filter(username__iexact=username)  # thisIsMyUsername == thisismyusername
        if not qs.exists():
            raise forms.ValidationError("This is an invalid user.")
        # if qs.count() != 1:
        #     raise forms.ValidationError("This is an invalid user.")
        return username
