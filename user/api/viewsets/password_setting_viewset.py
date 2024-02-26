from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from user.api.serializers import ChangePasswordRequestSerializer
from user.utils import send_reset_password_email_task
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import generics, status
from user.api.serializers import ChangePasswordActionSerializer
from drf_spectacular.utils import extend_schema
import jwt


@extend_schema(tags=["Change Password"])
class ChangePasswordRequestViewSet(generics.GenericAPIView):
    serializer_class = ChangePasswordRequestSerializer
    def post(self, request):
        serializer: ChangePasswordRequestSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = jwt.encode(payload={"user_id": user.id},
                              key='secret',
                              algorithm="HS256")
        current_site = 'http://localhost:8000'
        url = f'{current_site}/change-password-action?token={str(token)}'

        send_reset_password_email_task(user.email, url)

        response_data = {
            'success': True,
            'message': 'Reset Password Email hs been sent',
            'token': str(token)
        }
        serializer_data = {
            'token': token,
            'password': serializer.validated_data['password'],
            'repeat_password': serializer.validated_data['repeat_password'],
        }

        # ارسال درخواست به ویو ChangePasswordActionViewSet
        ChangePasswordActionViewSet(data=serializer_data)
        return Response(data=response_data, status=status.HTTP_200_OK)   



@extend_schema(tags=["Change Password"])
class ChangePasswordActionViewSet(generics.GenericAPIView):
    serializer_class = ChangePasswordActionSerializer
    
    def get(self, request, *args, **kwargs):
        token= request.query_params.get('token')
        user_data = {
            'token': token,
        }
        return Response(data=user_data, status=status.HTTP_200_OK)
    
    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.context['token'] = self.request.query_params.get('token')
        return serializer
    
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = {
            'detail': 'Password reset successfully'
        }

        return Response(
            data=response_data,
            status=status.HTTP_200_OK )



