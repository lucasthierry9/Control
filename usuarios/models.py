from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

#adicionar super user pelo "/admin" no navegador
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário precisa ter is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
#adicionar super user pelo "/admin" no navegador

class Usuario(AbstractUser):
    TIPO_USUARIO = (
        ('empresa', 'Empresa'),
        ('funcionario', 'Funcionário'),
    )

    razao_social = models.CharField(max_length=50)
    nome_fantasia = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=14, unique=True, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    telefone = models.CharField(max_length=11)
    tipo = models.CharField(max_length=20, choices=TIPO_USUARIO, default='empresa')
    username = None
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UsuarioManager()  # <---- adiciona o novo manager aqui
