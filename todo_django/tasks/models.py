from django.db import models
from user_account.models import User
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=70, blank=False, )
    description = models.TextField()

    STATUS_CHOICE = {
        "pending":"Pending",
        "in_process" : "In Process",
        "completed" : "Completed",
    }
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICE,
        default="pending")

    PRIORITY_CHOICES = {
        "low" : "Low",
        "medium" : "Medium",
        "high" : "High",
    }
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="medium")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="tasks",
        verbose_name= "Task Owner"
    )

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return self.title
    
    def mark_complete(self):
        """
        Mark the task as completed and set completion timestamp.
        """
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        """
        Mark the task as pending and clear completion timestamp.
        """
        self.status = 'pending'
        self.completed_at = None
        self.save()
    
    def toggle_complete(self):
        """
        Toggle task completion status.
        """
        if self.status == 'completed':
            self.mark_incomplete()
        else:
            self.mark_complete()
    
    @property
    def is_overdue(self):
        """
        Check if the task is overdue.
        Returns True if task has a due date in the past and is not completed.
        """
        if self.due_date and self.status != 'completed':
            from datetime import date
            return self.due_date < date.today()
        return False
    
    @property
    def is_completed(self):
        """
        Check if the task is completed.
        """
        return self.status == 'completed'
    
    def set_priority(self, priority):
        """
        Set task priority with validation.
        """
        valid_priorities = [choice[0] for choice in self.PRIORITY_CHOICES]
        if priority in valid_priorities:
            self.priority = priority
            self.save()
        else:
            raise ValueError(f"Priority must be one of: {valid_priorities}")
    
    def set_status(self, status):
        """
        Set task status with validation.
        If status is 'completed', also set completed_at timestamp.
        """
        valid_statuses = [choice[0] for choice in self.STATUS_CHOICES]
        if status in valid_statuses:
            self.status = status
            if status == 'completed' and not self.completed_at:
                self.completed_at = timezone.now()
            elif status != 'completed':
                self.completed_at = None
            self.save()
        else:
            raise ValueError(f"Status must be one of: {valid_statuses}")
