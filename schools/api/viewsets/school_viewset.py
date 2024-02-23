from rest_framework import viewsets,generics
from schools.models import School
from schools.api.serializers import SchoolSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication


class SchoolApiViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    http_method_names = ['get','post','put','patch']
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    
    def get_permissions(self):
        if self.action in ['partial_update','create','update']:
            return [IsAdminUser()]
        
        return super().get_permissions()
