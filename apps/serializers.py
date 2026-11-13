from django.contrib.auth import password_validation
from rest_framework import serializers

from apps.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'date_joined']
        read_only_fields = ['id', 'is_staff', 'date_joined']

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance



class CalculatorSerializer(serializers.Serializer):
    """Query parametrlarni tekshirish: ?n1=5&n2=7"""
    n1 = serializers.IntegerField(help_text='1-son')
    n2 = serializers.IntegerField(help_text='2-son')


class CalculatorResultSerializer(serializers.Serializer):
    result = serializers.IntegerField()
