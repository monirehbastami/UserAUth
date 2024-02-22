from django.urls import path,include
from rest_framework.routers import DefaultRouter
from schools.api.viewsets import SchoolApiViewSet,CreateSchoolApiView


router = DefaultRouter()
router.register('list-schools',SchoolApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('retrieve-school',CreateSchoolApiView.as_view(),name='create-school')
]