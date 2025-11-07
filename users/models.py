from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
import uuid
import random


class User(AbstractUser):
    ROLE_CHOICES = [
        ("GeneralPublic", "General Public"),
        ("Student", "Student"),
        ("Staff", "Staff"),
        ("Admin", "Admin"),
    ]

    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default="GeneralPublic")
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)  # after OTP verification

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Automatically assign Django group when user is saved
        group, _ = Group.objects.get_or_create(name=self.role)
        self.groups.add(group)

    def __str__(self):
        return f"{self.username} ({self.role})"


class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp_record")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def generate_otp(self):
        """Generate and save a new random 6-digit OTP"""
        otp_value = str(random.randint(100000, 999999))
        self.otp = otp_value
        self.created_at = timezone.now()
        self.is_used = False
        self.save()
        return otp_value

    def is_valid(self):
        """Check if OTP is still valid (10 min window)"""
