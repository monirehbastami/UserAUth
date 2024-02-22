from rest_framework import viewsets,generics
from schools.models import School
from schools.api.serializers import SchoolSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class SchoolApiViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    http_method_names = ['get']
    

class CreateSchoolApiView(generics.CreateAPIView,generics.UpdateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user


class RetrieveSchoolApiView(generics.RetrieveUpdateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user