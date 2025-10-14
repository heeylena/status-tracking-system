"""
Models for Employee Status Tracking System.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone


class Employee(models.Model):
    """
    Represents an employee in the system.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
    
    def __str__(self):
        return self.name
    
    def get_current_status_log(self):
        """Get the current active status log for this employee."""
        return self.status_logs.filter(end_time__isnull=True).first()
    
    def soft_delete(self):
        """Soft delete the employee by setting is_active to False."""
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()


class Status(models.Model):
    """
    Represents a status type that can be assigned to employees.
    """
    # Validate HEX color format
    color_validator = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message='Color must be a valid HEX color code (e.g., #3b82f6)'
    )
    
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, validators=[color_validator])
    has_end_time = models.BooleanField(
        default=False,
        help_text='Does this status require a planned end time?'
    )
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
    
    def __str__(self):
        return self.name


class StatusLog(models.Model):
    """
    Logs status changes for employees with time tracking.
    """
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='status_logs'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status_logs'
    )
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    planned_end_time = models.DateTimeField(null=True, blank=True)
    overdue_duration = models.IntegerField(
        default=0,
        help_text='Overdue duration in seconds, calculated when status ends'
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    class Meta:
        ordering = ['-start_time']
        verbose_name = 'Status Log'
        verbose_name_plural = 'Status Logs'
        indexes = [
            models.Index(fields=['employee', '-start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['planned_end_time']),
        ]
    
    def __str__(self):
        return f"{self.employee.name} - {self.status.name} ({self.start_time})"
    
    def get_elapsed_seconds(self):
        """Calculate elapsed time in seconds from start_time to now or end_time."""
        end = self.end_time or timezone.now()
        return int((end - self.start_time).total_seconds())
    
    def get_remaining_seconds(self):
        """Calculate remaining time in seconds until planned_end_time."""
        if not self.planned_end_time:
            return None
        if self.end_time:
            # For ended logs, use end_time
            return int((self.planned_end_time - self.end_time).total_seconds())
        # For active logs, use current time
        return int((self.planned_end_time - timezone.now()).total_seconds())
    
    def is_overdue(self):
        """Check if the status is overdue."""
        if not self.planned_end_time:
            return False
        if self.end_time:
            return self.end_time > self.planned_end_time
        return timezone.now() > self.planned_end_time
    
    def get_overdue_seconds(self):
        """Calculate how many seconds overdue (negative of remaining_seconds if overdue)."""
        if not self.is_overdue():
            return 0
        remaining = self.get_remaining_seconds()
        return abs(remaining) if remaining is not None else 0
    
    def calculate_and_save_overdue_duration(self):
        """
        Calculate overdue duration and save it when closing this log.
        This should be called when setting end_time.
        """
        if self.planned_end_time and self.end_time:
            if self.end_time > self.planned_end_time:
                self.overdue_duration = int((self.end_time - self.planned_end_time).total_seconds())
            else:
                self.overdue_duration = 0
