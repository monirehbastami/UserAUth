from rest_framework import viewsets,generics
from user.api.serializers import SchoolStaffSerializer,SchoolStaffRetrieveSerializer
from user.models import SchoolStaff
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers


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
        if self.action == 'list':
            return SchoolStaffSerializer
        if self.action in ['create','update','partial_update']:
            return SchoolStaffRetrieveSerializer
        return super().get_serializer_class()
    
class AdminSchoolStaffApiViewSet(viewsets.ModelViewSet):
    queryset = SchoolStaff.school_staffs.all()
    http_method_names = ['get','post','put','patch']
    serializer_class = SchoolStaffSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['partial_update','create','update']:
            return [IsAdminUser()]
        
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SchoolStaffSerializer
        if self.action == 'retrieve':
            return SchoolStaffRetrieveSerializer
        return super().get_serializer_class()