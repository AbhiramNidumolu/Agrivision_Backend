from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import OTPVerification
from django.core.mail import send_mail
from django.conf import settings
import random

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        """Ensure email belongs to the college domain robustly."""
        email = value.strip().replace("\r", "").replace("\n", "").lower()
        if not email.endswith("@vitapstudent.ac.in"):
            raise serializers.ValidationError("Please use your campus email ID.")
        return email


    def create(self, validated_data):
        # Extract role and password
        role = validated_data.pop("role", "GeneralPublic")
        password = validated_data.pop("password")

        # Create inactive user
        user = User(**validated_data)
        user.set_password(password)
        user.role = role
        user.is_active = False  # wait for OTP verification
        user.save()

        # Assign to role-based group
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        # Create OTP
        otp, _ = OTPVerification.objects.get_or_create(user=user)
        otp_code = str(random.randint(100000, 999999))
        otp.otp = otp_code
        otp.save()

        # Send OTP email
        send_mail(
            subject="AgriVision Email Verification",
            message=f"Hello {user.username},\n\nYour OTP for verification is: {otp_code}\n\n- AgriVision Team",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )

        return user


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get("email")
        otp = data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_record = OTPVerification.objects.get(user=user, otp=otp, is_used=False)
        except (User.DoesNotExist, OTPVerification.DoesNotExist):
            raise serializers.ValidationError("Invalid OTP or email.")

        # Mark OTP as used and activate user
        otp_record.is_used = True
        otp_record.save()

        user.is_active = True
        user.is_verified = True
        user.save()

        data["user"] = user
        return data
