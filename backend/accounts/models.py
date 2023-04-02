from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import CustomUserManager
from django.contrib.auth.models import PermissionsMixin


class App_User(AbstractBaseUser, PermissionsMixin):
    username = None

    class Types(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        PROFESSOR = 'PROFESSOR', 'Professor'

    type = models.CharField(max_length=50, choices=Types.choices, default=Types.STUDENT)

    email = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    dept_name = models.CharField(max_length=255)
    contact_number = PhoneNumberField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Student_manager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=App_User.Types.STUDENT)


class Student(App_User):
    base_type = App_User.Types.STUDENT
    objects = Student_manager()

    @property
    def more(self):
        return StudentMore
    
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = App_User.Types.STUDENT
        return super().save(*args, **kwargs)


class StudentMore(models.Model):
    user = models.OneToOneField(Student, on_delete=models.CASCADE)
    accademic_year = models.IntegerField()
    cv = models.FileField(upload_to='student_cv/', blank=True, null=True)


class Professor_manager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=App_User.Types.PROFESSOR)


class Professor(App_User):
    base_type = App_User.Types.PROFESSOR
    objects = Professor_manager()

    @property
    def more(self):
        return ProfessorMore
    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.type = App_User.Types.PROFESSOR
        return super().save(*args, **kwargs)

class ProfessorMore(models.Model):
    user = models.OneToOneField(Professor, on_delete=models.CASCADE)
    joining_year = models.IntegerField()
    designation = models.CharField(max_length=255)
    cv = models.FileField(upload_to='professor_cv/', blank=True, null=True)