from django.urls import path,include
from user.api import viewsets
from rest_framework.routers import DefaultRouter
from user.api import viewsets

router = DefaultRouter()
router.register('school-staffs',viewsets.SchoolStaffApiViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('create-school-staff',viewsets.CreateSchoolStaffApiView.as_view(),
         name='create-school-staff'),
]