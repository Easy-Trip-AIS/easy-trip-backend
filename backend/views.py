import requests
from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer, LoginSerializer, RecommendSerializer, UserSerializer, LogoutSerializer
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

class LogoutView(APIView):
    """
    Приймає POST { refresh: "<refresh_token>" }
    та блокує цей токен (додає до token_blacklist).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data['refresh']
        try:
            # блокуємо рефреш-токен
            RefreshToken(refresh_token).blacklist()
        except Exception:
            return Response(
                {"detail": "Невдалось заблокувати токен."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # повертаємо 205 No Content
        return Response(status=status.HTTP_205_RESET_CONTENT)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Повертає дані поточного користувача у форматі UserSerializer.
        """
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

# ------------------------------------------------------------------------------------------------------------

# URL вашого ML-сервісу
ML_SERVICE_URL = 'http://127.0.0.1:8001/ml/recommend'


class RecommendView(APIView):
    def post(self, request):
        serializer = RecommendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        try:
            ml_resp = requests.post(
                ML_SERVICE_URL,
                json=payload,
                timeout=100
            )
            ml_resp.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {
                    "detail": "Не вдалося зв’язатися з ML-сервісом",
                    "error": str(e)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Повертаємо ті ж дані, які надіслав наш ML
        return Response(ml_resp.json(), status=ml_resp.status_code)