from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email',
            'first_name', 'last_name',
            'avatar', 'phone', 'city', 'plan', 'created_at',
            'is_staff',
            'is_superuser',
        ]
        read_only_fields = ['id', 'created_at', 'plan', 'is_staff', 'is_superuser']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def validate(self, attrs):
        # يطبّق مدققات كلمة المرور في settings (كلمة شائعة، أرقام فقط، شبيهة بالاسم...)
        candidate = User(**{k: v for k, v in attrs.items() if k != 'password'})
        try:
            validate_password(attrs['password'], user=candidate)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': list(exc.messages)})
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
