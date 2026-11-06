from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """مستخدم مخصص يوسّع AbstractUser."""
    PLAN_CHOICES = [
        ('free', 'مجاني'),
        ('pro', 'Pro'),
        ('business', 'Business'),
    ]

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.username