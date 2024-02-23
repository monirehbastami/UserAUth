from rest_framework import viewsets
from user.api.serializers import SchoolStaffSerializer
from user.models import SchoolStaff
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication


class SchoolStaffApiViewSet(viewsets.ModelViewSet):
    queryset = SchoolStaff.school_staffs.all()
    http_method_names = ['get','post','put','patch']
    serializer_class = SchoolStaffSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    def get_permissions(self):
        if self.action in ['partial_update','create','update']:
            return [IsAdminUser()]
        
        return super().get_permissions()
    
