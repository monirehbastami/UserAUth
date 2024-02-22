from rest_framework import viewsets,generics
from user.api.serializers import SchoolStaffSerializer
from user.models import SchoolStaff


class SchoolStaffApiViewSet(viewsets.ModelViewSet):
    queryset = SchoolStaff.school_staffs.all()
    http_method_names = ['get']
    serializer_class = SchoolStaffSerializer

class CreateSchoolStaffApiView(generics.CreateAPIView):
    serializer_class = SchoolStaffSerializer