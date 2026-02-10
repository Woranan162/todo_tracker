from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
)
from user_account.permissions import IsOwner


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing tasks.
    Handles all CRUD operations and custom actions.

    Endpoints:
    GET    /api/tasks/              - List all tasks
    POST   /api/tasks/              - Create task
    GET    /api/tasks/{id}/         - Get task detail
    PATCH  /api/tasks/{id}/         - Update task
    DELETE /api/tasks/{id}/         - Delete task
    POST   /api/tasks/{id}/complete/ - Toggle completion
    GET    /api/tasks/overdue/      - List overdue tasks
    GET    /api/tasks/today/        - List tasks due today
    """
    permission_classes = [IsAuthenticated, IsOwner]

    # Filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority', 'status']
    ordering = ['-created_at']  # Default ordering

    def get_queryset(self):
        """
        Return tasks belonging to the current user only.
        """
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        """
        Return different serializers based on action.
        - create: TaskCreateSerializer
        - update/partial_update: TaskUpdateSerializer
        - everything else: TaskSerializer
        """
        if self.action == 'create':
            return TaskCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        return TaskSerializer

    def get_permissions(self):
        """
        Return different permissions based on action.
        - create and list: Only IsAuthenticated needed
        - others: IsAuthenticated + IsOwner
        """
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]

    def create(self, request, *args, **kwargs):
        """
        Create a new task.
        POST /api/tasks/
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            task = serializer.save()

            # Return full task details using TaskSerializer
            response_serializer = TaskSerializer(task)
            return Response(
                {
                    "status": "success",
                    "message": "Task created successfully.",
                    "task": response_serializer.data,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "status": "error",
                "message": "Task creation failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def list(self, request, *args, **kwargs):
        """
        List all tasks for current user.
        GET /api/tasks/
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = TaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TaskSerializer(queryset, many=True)
        return Response(
            {
                "status": "success",
                "count": queryset.count(),
                "tasks": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        """
        Get a single task detail.
        GET /api/tasks/{id}/
        """
        task = self.get_object()
        serializer = TaskSerializer(task)
        return Response(
            {
                "status": "success",
                "task": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        """
        Update a task partially.
        PATCH /api/tasks/{id}/
        """
        task = self.get_object()
        serializer = TaskUpdateSerializer(
            task,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            updated_task = serializer.save()

            # Return full task details
            response_serializer = TaskSerializer(updated_task)
            return Response(
                {
                    "status": "success",
                    "message": "Task updated successfully.",
                    "task": response_serializer.data,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": "error",
                "message": "Task update failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete a task permanently.
        DELETE /api/tasks/{id}/
        """
        task = self.get_object()
        task_title = task.title
        task.delete()

        return Response(
            {
                "status": "success",
                "message": f"Task '{task_title}' deleted successfully.",
            },
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='complete')
    def toggle_complete(self, request, pk=None):
        """
        Toggle task completion status.
        POST /api/tasks/{id}/complete/
        """
        task = self.get_object()
        task.toggle_complete()

        # Build response message
        if task.status == 'completed':
            message = "Task marked as completed."
        else:
            message = "Task marked as incomplete."

        serializer = TaskSerializer(task)
        return Response(
            {
                "status": "success",
                "message": message,
                "task": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue(self, request):
        """
        List all overdue tasks for current user.
        GET /api/tasks/overdue/
        """
        from datetime import date
        overdue_tasks = self.get_queryset().filter(
            due_date__lt=date.today(),
            status__in=['pending', 'in_progress']
        )

        serializer = TaskSerializer(overdue_tasks, many=True)
        return Response(
            {
                "status": "success",
                "count": overdue_tasks.count(),
                "tasks": serializer.data,
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        """
        List all tasks due today for current user.
        GET /api/tasks/today/
        """
        from datetime import date
        today_tasks = self.get_queryset().filter(
            due_date=date.today()
        )

        serializer = TaskSerializer(today_tasks, many=True)
        return Response(
            {
                "status": "success",
                "count": today_tasks.count(),
                "tasks": serializer.data,
            },
            status=status.HTTP_200_OK
        )