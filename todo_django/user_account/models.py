from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(blank=True, unique=True, null=True)
    first_name = models.CharField(max_length=150,blank=False)
    last_name = models.CharField(max_length=150,blank=False)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Returns the short name for the user (first name).
        """
        return self.first_name
    
    def can_change_username(self):
        if self.last_username_change is None:
            return True
        weeks_since_change = (timezone.now() - self.last_username_change).days / 7
        return weeks_since_change >= 2

    def days_until_username_change(self):
        if self.can_change_username():
            return 0
        days_passed = (timezone.now() - self.last_username_change).days
        return 14 - days_passed  # 14 days = 2 weeks