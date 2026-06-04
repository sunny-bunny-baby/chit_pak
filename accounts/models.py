from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser