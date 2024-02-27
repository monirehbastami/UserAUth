from rest_framework import viewsets,status
from rest_framework.response import Response
from user.api.serializers import SchoolStaffSerializer,SchoolStaffRetrieveSerializer,ActiveUserSerializer
from user.models import SchoolStaff,User
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from user.utils import send_activation_email
import jwt
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed




class SchoolStaffApiViewSet(viewsets.ModelViewSet):
    queryset = SchoolStaff.school_staffs.all()
    http_method_names = ['get','post','put','patch']
    serializer_class = SchoolStaffSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        if self.action in ['create','update','partial_update']:
            return self.request.user
        return super().get_object()
        

    def get_serializer_class(self):
        if self.action in ['list','create']:
            return SchoolStaffSerializer
        if self.action in ['update','partial_update']:
            return SchoolStaffRetrieveSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        user = serializer.save()
        token = jwt.encode(payload={"user_id": user.id},
                              key='secret',
                              algorithm="HS256")
        current_site = 'http://localhost:8000'
        url = f'{current_site}/active-user?token={str(token)}'
        send_activation_email(user)
        
        response_data = {
            'success': True,
            'message': 'Activation link has been sent',
            'token': str(token)
        }
        return Response(data=response_data, status=status.HTTP_200_OK)   


class AdminSchoolStaffApiViewSet(viewsets.ModelViewSet):
    queryset = SchoolStaff.school_staffs.all()
    http_method_names = ['get','post','put','patch','delete']
    serializer_class = SchoolStaffSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['partial_update','create','update','delete']:
            return [IsAdminUser()]
        
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SchoolStaffSerializer
        if self.action == 'retrieve':
            return SchoolStaffRetrieveSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        user = serializer.save()
        token = jwt.encode(payload={"user_id": user.id},
                              key='secret',
                              algorithm="HS256")
        current_site = 'http://localhost:8000'
        url = f'{current_site}/active-user?token={str(token)}'
        send_activation_email(user,url)
        
        response_data = {
            'success': True,
            'message': 'Activation link has been sent',
            'token': str(token)
        }
        return Response(data=response_data, status=status.HTTP_200_OK) 
    
class ActiveUser(generics.GenericAPIView):
    serializer_class = ActiveUserSerializer
    
    def get_serializer(self,*args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        token= self.request.query_params.get('token')
        serializer.fields['token'].default = token
        serializer.fields['token'].initial = token
        serializer.fields['token'].required = False    
        return serializer
    def perform_authentication(self, request):
        # Custom authentication logic
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = serializer.validated_data['token']
            decoded_data = jwt.decode(jwt=token, key='secret', algorithms=["HS256"])
            user_id = decoded_data.get('user_id')
            user = User.objects.get(id=user_id)
            user.is_email_confirmed = True
            user.save()
        except Exception:
            raise AuthenticationFailed('The reset link is invalid', 401)

    def get(self, request):
        response_data = {
            'detail': 'User activated successfully'
        }
        return Response(data=response_data, status=status.HTTP_200_OK)