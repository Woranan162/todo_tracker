from rest_framework import serializers
from datetime import date
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for reading task details.
    Includes computed properties and user info.
    """
    is_overdue = serializers.BooleanField(read_only=True)
    is_completed = serializers.BooleanField(read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'created_at',
            'updated_at',
            'completed_at',
            'is_overdue',
            'is_completed',
            'owner',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'completed_at',
            'is_overdue',
            'is_completed',
            'owner',
        ]

    def get_owner(self, obj):
        """
        Returns basic owner information.
        """
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'full_name': obj.user.get_full_name(),
        }


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new tasks.
    User is set automatically from request.
    Warns if due date is in the past.
    """
    warning = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'warning',
        ]
        read_only_fields = ['id', 'warning']

    def get_warning(self, obj):
        """
        Returns warning message if due date is in the past.
        """
        if obj.due_date and obj.due_date < date.today():
            return "Warning: Due date is in the past."
        return None

    def validate_title(self, value):
        """
        Validate title is not empty or just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty or just whitespace."
            )
        return value.strip()

    def create(self, validated_data):
        """
        Create task and automatically assign
        logged-in user as owner.
        """
        # Get user from request context
        user = self.context['request'].user
        task = Task.objects.create(user=user, **validated_data)
        return task


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing tasks.
    All fields are optional (partial updates).
    Warns if due date is in the past.
    """
    warning = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'warning',
        ]
        read_only_fields = ['id', 'warning']

    def get_warning(self, obj):
        """
        Returns warning message if due date is in the past.
        """
        if obj.due_date and obj.due_date < date.today():
            return "Warning: Due date is in the past."
        return None

    def validate_title(self, value):
        """
        Validate title is not empty or just whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError(
                "Title cannot be empty or just whitespace."
            )
        return value.strip()

    def update(self, instance, validated_data):
        """
        Update task fields.
        Handles status change to completed automatically.
        """
        # Check if status is being changed to completed
        new_status = validated_data.get('status', instance.status)

        if new_status == 'completed' and instance.status != 'completed':
            # Use model method to handle completion
            instance.mark_complete()
            # Remove status from validated_data since mark_complete handles it
            validated_data.pop('status', None)

        elif new_status != 'completed' and instance.status == 'completed':
            # Use model method to handle un-completion
            instance.mark_incomplete()
            validated_data.pop('status', None)

        # Update remaining fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance