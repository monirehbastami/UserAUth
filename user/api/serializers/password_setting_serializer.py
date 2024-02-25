from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from jwt import decode
from django.conf import settings
from user.models import User
import os
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
import jwt


class ChangePasswordRequestSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages['required'] = f'Field\
                `{field.label}` is requires'

    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise ValidationError(
                {
                    'detail': "There is no user with provided email"
                }
            )
        attrs['user'] = user
        return super().validate(attrs)


class ChangePasswordActionSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.error_messages['required'] = f'Field \
                `{field.label}`is required'

    token = serializers.CharField(max_length=600)
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    repeat_password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    class Meta:
        fields = ['password', 'repeat_password', 'token']

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError(
                {'detail': "Passwords does not match"}
            )
        
        try:
            password = attrs['password']
            token = attrs['token']
            decoded_data = jwt.decode(jwt=token,
                                key='secret',
                                algorithms=["HS256"])
            user_id = decoded_data.get('user_id')
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            
            return super().validate(attrs)
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)
    