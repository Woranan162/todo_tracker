from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# Create router and register TaskViewSet
router = DefaultRouter()
router.register(r'', TaskViewSet, basename='task')

app_name = 'tasks'

urlpatterns = [
    path('', include(router.urls)),
]