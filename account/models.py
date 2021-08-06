# Creating a custom model for user administration


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, firstname, lastname, username, email, password):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),  # this will convert email to small letter if capital letter is entered
            username=username,
            firstname=firstname,
            lastname=lastname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            firstname=firstname,
            lastname=lastname,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # specify that the email should be the username field
    REQUIRED_FIELDS = ['username', 'firstname',
                       'lastname']  # specifiy the fields that should pop when using creatsuperuser command

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_fullname(self):
        return self.firstname + " " + self.lastname

    # must include this
    def has_perm(self, perm, obj=None):
        return self.is_admin  # means if user is specified as admin, he should be able to do everything

    # Must include this function too
    def has_module_perms(self, add_label):
        return True


class Profile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=5)
    phone_number = models.CharField(blank=True, max_length=15)
    company = models.CharField(blank=True, max_length=100)
    company_description = models.TextField(blank=True)
    company_address = models.TextField(blank=True)

    def __str__(self):
        return self.user.firstname


@receiver(post_save, sender=MyUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=MyUser)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
