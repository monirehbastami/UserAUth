from user.api.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import AllowAny
from user.api.serializers import ResetPasswordSerializer
from user.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.core import cache
from user.utils import send_otp_email
import random

from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = ResetPasswordSerializer

    def post(self,request,*args,**kwargs):
        ser = self.serializer_class(data=request.data)
        ser.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=ser.validated_data.get('email'))
        except User.DoesNotExist:
            return Response({"msg":"User not Found!"},status=status.HTTP_400_BAD_REQUEST)
        except User.MultipleObjectsReturned:
            return Response({"msg":"multiple not Found!"},status=status.HTTP_400_BAD_REQUEST)
        user_otp = ser.validated_data.get("otp",None)
        new_password = ser.validated_data.get("new_password",None)
        cache_prefix = ser.validated_data("email")+"_otp"

        if not user_otp:
            cached_otp  = cache.get(cache_prefix,None)
            if not cached_otp:
                random.seed()
                otp = str(random.randint(111111,999999))
                print("otp: "+otp)
                send_otp_email(otp,user.email)
                cache.set(cache_prefix,otp,timeout=90)
                return Response({"msg":"otp send"},status=status.HTTP_200_OK)
            else:
                return Response({"msg":"otp already send"},status=status.HTTP_400_BAD_REQUEST)
            
        if not user_otp or not new_password:
            return Response({"msg":"must include otp and new password"},status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(cache_prefix,None)
        if not str(user_otp) == cached_otp:
            return Response({"msg":"invalid otp"},status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        cache.delete(cache_prefix)
        return Response({"msg":"new password save"},status=status.HTTP_200_OK)
