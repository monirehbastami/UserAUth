from rest_framework import viewsets,generics
from user.api.serializers import SchoolStaffSerializer
from user.models import SchoolStaff
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication


class SchoolStaffApiViewSet(viewsets.ModelViewSet):
    queryset = SchoolStaff.school_staffs.all()
    http_method_names = ['get','post','put','patch']
    serializer_class = SchoolStaffSerializer
    
    
