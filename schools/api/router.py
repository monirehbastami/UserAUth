from django.urls import path,include
from rest_framework.routers import DefaultRouter
from schools.api.viewsets import SchoolApiViewSet


router = DefaultRouter()
router.register('schools',SchoolApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
]