"""
Serializers for Employee Status Tracking System API.
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Employee, Status, StatusLog


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for Status model."""
    
    class Meta:
        model = Status
        fields = ['id', 'name', 'color', 'has_end_time', 'display_order', 'is_active']
        read_only_fields = ['id']


class CurrentStatusSerializer(serializers.ModelSerializer):
    """Serializer for current status information with real-time calculations."""
    
    status_name = serializers.CharField(source='status.name', read_only=True)
    status_color = serializers.CharField(source='status.color', read_only=True)
    elapsed_seconds = serializers.SerializerMethodField()
    remaining_seconds = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    overdue_seconds = serializers.SerializerMethodField()
    
    class Meta:
        model = StatusLog
        fields = [
            'id', 'status_name', 'status_color', 'start_time',
            'planned_end_time', 'elapsed_seconds', 'remaining_seconds',
            'is_overdue', 'overdue_seconds', 'notes'
        ]
    
    def get_elapsed_seconds(self, obj):
        """Get elapsed time in seconds."""
        return obj.get_elapsed_seconds()
    
    def get_remaining_seconds(self, obj):
        """Get remaining time in seconds (can be negative if overdue)."""
        return obj.get_remaining_seconds()
    
    def get_is_overdue(self, obj):
        """Check if status is overdue."""
        return obj.is_overdue()
    
    def get_overdue_seconds(self, obj):
        """Get overdue duration in seconds."""
        return obj.get_overdue_seconds()


class EmployeeListSerializer(serializers.ModelSerializer):
    """Serializer for employee list with current status."""
    
    current_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'current_status', 'is_active']
    
    def get_current_status(self, obj):
        """Get current active status log."""
        current_log = obj.get_current_status_log()
        if current_log:
            return CurrentStatusSerializer(current_log).data
        return None


class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for employee with current status."""
    
    current_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = ['id', 'name', 'email', 'is_active', 'created_at', 'current_status']
        read_only_fields = ['id', 'created_at']
    
    def get_current_status(self, obj):
        """Get current active status log."""
        current_log = obj.get_current_status_log()
        if current_log:
            return CurrentStatusSerializer(current_log).data
        return None


class StatusLogSerializer(serializers.ModelSerializer):
    """Serializer for status log history."""
    
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    status_name = serializers.CharField(source='status.name', read_only=True)
    status_color = serializers.CharField(source='status.color', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    duration_seconds = serializers.SerializerMethodField()
    
    class Meta:
        model = StatusLog
        fields = [
            'id', 'employee_name', 'status_name', 'status_color',
            'start_time', 'end_time', 'planned_end_time', 'overdue_duration',
            'duration_seconds', 'notes', 'created_by_username'
        ]
    
    def get_duration_seconds(self, obj):
        """Get total duration of this status log."""
        if obj.end_time:
            return int((obj.end_time - obj.start_time).total_seconds())
        # For active logs, calculate from start_time to now
        return obj.get_elapsed_seconds()


class ChangeStatusSerializer(serializers.Serializer):
    """Serializer for changing employee status."""
    
    status_id = serializers.IntegerField(required=True)
    planned_end_time = serializers.DateTimeField(required=False, allow_null=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate_status_id(self, value):
        """Validate that status exists and is active."""
        try:
            status = Status.objects.get(id=value, is_active=True)
        except Status.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive status.")
        return value
    
    def validate_planned_end_time(self, value):
        """Validate that planned_end_time is in the future."""
        if value and value < timezone.now():
            raise serializers.ValidationError("Planned end time must be in the future.")
        return value
    
    def validate(self, data):
        """Cross-field validation."""
        status_id = data.get('status_id')
        planned_end_time = data.get('planned_end_time')
        
        try:
            status = Status.objects.get(id=status_id)
            if status.has_end_time and not planned_end_time:
                raise serializers.ValidationError({
                    'planned_end_time': f'Status "{status.name}" requires a planned end time.'
                })
        except Status.DoesNotExist:
            pass
        
        return data


class EmployeeStatisticsSerializer(serializers.Serializer):
    """Serializer for employee time statistics."""
    
    status_name = serializers.CharField()
    status_color = serializers.CharField()
    total_seconds = serializers.IntegerField()
    count = serializers.IntegerField()
    total_overdue_seconds = serializers.IntegerField()
