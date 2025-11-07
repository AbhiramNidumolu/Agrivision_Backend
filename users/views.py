from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from .serializers import UserSerializer, OTPVerifySerializer

User = get_user_model()


# ✅ SIGNUP VIEW – Creates inactive user & sends OTP
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Signup successful! OTP sent to your campus email."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ OTP VERIFICATION VIEW
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            return Response(
                {"message": "Account verified successfully! You can now log in."},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ LOGIN VIEW – Authenticates verified users only
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", None)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "No account found for this email."}, status=400)

        # Authenticate using Django’s system
        user = authenticate(username=user.username, password=password)
        if not user:
            return Response({"error": "Invalid credentials."}, status=400)

        if not user.is_active:
            return Response({"error": "Please verify your account via OTP before login."}, status=403)

        if role and user.role != role:
            return Response({"error": f"This account is not registered as {role}."}, status=403)

        # Issue token for session management
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
            "email": user.email,
        }, status=status.HTTP_200_OK)
