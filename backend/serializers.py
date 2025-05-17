from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    date_of_birth = serializers.DateField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'password')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # attrs приходять як {'username':..., 'password':...}
        # якщо фронт шле {'login':..., 'password':...}, то раніше у view ми їх перейменуємо
        return super().validate(attrs)

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="Refresh-токен, який потрібно заблокувати"
    )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # перелік полів, які хочете бачити у профілі
        fields = (
            'username',        # login
            'email',
            'first_name',      # name
            'last_name',       # surname
            'date_of_birth',
            'date_joined',
        )
        read_only_fields = fields

# ------------------------------------------------------------------------------------------------------------

class LocationSerializer(serializers.Serializer):
    lat = serializers.FloatField(help_text="Широта")
    lng = serializers.FloatField(help_text="Довгота")

class PreferencesSerializer(serializers.Serializer):
    culture       = serializers.FloatField(min_value=0.0, max_value=1.0)
    nature        = serializers.FloatField(min_value=0.0, max_value=1.0)
    food          = serializers.FloatField(min_value=0.0, max_value=1.0)
    shopping      = serializers.FloatField(min_value=0.0, max_value=1.0)
    relaxation    = serializers.FloatField(min_value=0.0, max_value=1.0)
    spiritual     = serializers.FloatField(min_value=0.0, max_value=1.0)
    entertainment = serializers.FloatField(min_value=0.0, max_value=1.0)

class RecommendSerializer(serializers.Serializer):
    start_location      = LocationSerializer()
    end_location        = LocationSerializer()
    preferences         = PreferencesSerializer()
    transport           = serializers.ChoiceField(choices=['walk', 'car', 'bike'])
    free_time_minutes   = serializers.IntegerField(min_value=0, help_text="Доступний час у хвилинах")