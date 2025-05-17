from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, LoginSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# ------------------------------------------------------------------------------------------------------------

# backend/views.py

# backend/views.py

import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecommendSerializer

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