"""
Django Admin customization for Employee Status Tracking System.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Q
from .models import Employee, Status, StatusLog


class StatusLogInline(admin.TabularInline):
    """Inline admin for StatusLog."""
    model = StatusLog
    extra = 0
    fields = ['status', 'start_time', 'end_time', 'planned_end_time', 'overdue_duration', 'notes']
    readonly_fields = ['start_time', 'overdue_duration']
    can_delete = False


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin for Employee model."""
    list_display = ['name', 'email', 'current_status_display', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email']
    readonly_fields = ['created_at', 'deleted_at']
    inlines = [StatusLogInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email')
        }),
        ('Status', {
            'fields': ('is_active', 'created_at', 'deleted_at')
        }),
    )
    
    def current_status_display(self, obj):
        """Display current status with color."""
        current_log = obj.get_current_status_log()
        if current_log:
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
                current_log.status.color,
                current_log.status.name
            )
        return format_html('<span style="color: gray;">No Active Status</span>')
    current_status_display.short_description = 'Current Status'
    
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        """Export selected employees to Excel."""
        from openpyxl import Workbook
        from django.http import HttpResponse
        from datetime import datetime
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Employees"
        
        # Headers
        headers = ['Name', 'Email', 'Current Status', 'Is Active']
        ws.append(headers)
        
        # Data
        for emp in queryset:
            current_log = emp.get_current_status_log()
            current_status = current_log.status.name if current_log else 'N/A'
            ws.append([emp.name, emp.email or 'N/A', current_status, 'Yes' if emp.is_active else 'No'])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=employees_{datetime.now().strftime("%Y%m%d")}.xlsx'
        wb.save(response)
        return response
    export_to_excel.short_description = 'Export selected to Excel'


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """Admin for Status model."""
    list_display = ['name', 'color_display', 'has_end_time', 'display_order', 'is_active']
    list_filter = ['has_end_time', 'is_active']
    search_fields = ['name']
    ordering = ['display_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'color', 'has_end_time')
        }),
        ('Display Settings', {
            'fields': ('display_order', 'is_active')
        }),
    )
    
    def color_display(self, obj):
        """Display color swatch."""
        return format_html(
            '<div style="width: 50px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_display.short_description = 'Color'


class IsOverdueFilter(admin.SimpleListFilter):
    """Custom filter for overdue status logs."""
    title = 'overdue status'
    parameter_name = 'is_overdue'
    
    def lookups(self, request, model_admin):
        return (
            ('yes', 'Overdue'),
            ('no', 'Not Overdue'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(
                planned_end_time__isnull=False,
                end_time__isnull=True
            ).filter(planned_end_time__lt=timezone.now())
        elif self.value() == 'no':
            return queryset.filter(
                Q(planned_end_time__isnull=True) |
                Q(planned_end_time__gte=timezone.now()) |
                Q(end_time__isnull=False)
            )


@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    """Admin for StatusLog model."""
    list_display = [
        'employee', 'status', 'start_time', 'end_time',
        'duration_display', 'overdue_display', 'created_by'
    ]
    list_filter = [
        IsOverdueFilter,
        'status',
        'start_time',
        'employee',
    ]
    search_fields = ['employee__name', 'status__name', 'notes']
    readonly_fields = ['start_time', 'overdue_duration', 'created_by']
    date_hierarchy = 'start_time'
    
    fieldsets = (
        ('Status Information', {
            'fields': ('employee', 'status', 'created_by')
        }),
        ('Time Tracking', {
            'fields': ('start_time', 'end_time', 'planned_end_time', 'overdue_duration')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )
    
    def duration_display(self, obj):
        """Display duration in hours."""
        if obj.end_time:
            duration = (obj.end_time - obj.start_time).total_seconds()
        else:
            duration = (timezone.now() - obj.start_time).total_seconds()
        hours = duration / 3600
        return f"{hours:.2f}h"
    duration_display.short_description = 'Duration'
    
    def overdue_display(self, obj):
        """Display overdue duration with color."""
        if obj.overdue_duration > 0:
            hours = obj.overdue_duration / 3600
            return format_html(
                '<span style="color: red; font-weight: bold;">{:.2f}h</span>',
                hours
            )
        elif obj.is_overdue():
            # Currently overdue but not yet closed
            overdue_seconds = obj.get_overdue_seconds()
            hours = overdue_seconds / 3600
            return format_html(
                '<span style="color: red; font-weight: bold;">{:.2f}h (Active)</span>',
                hours
            )
        return format_html('<span style="color: green;">-</span>')
    overdue_display.short_description = 'Overdue'
    
    actions = ['export_to_excel']
    
    def export_to_excel(self, request, queryset):
        """Export selected status logs to Excel."""
        from openpyxl import Workbook
        from django.http import HttpResponse
        from datetime import datetime
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Status Logs"
        
        # Headers
        headers = ['Employee', 'Status', 'Start Time', 'End Time', 'Duration (hours)', 'Overdue (hours)', 'Notes']
        ws.append(headers)
        
        # Data
        for log in queryset:
            if log.end_time:
                duration = (log.end_time - log.start_time).total_seconds() / 3600
            else:
                duration = (timezone.now() - log.start_time).total_seconds() / 3600
            
            overdue = log.overdue_duration / 3600 if log.overdue_duration > 0 else 0
            
            ws.append([
                log.employee.name,
                log.status.name,
                log.start_time.strftime('%Y-%m-%d %H:%M:%S'),
                log.end_time.strftime('%Y-%m-%d %H:%M:%S') if log.end_time else 'Active',
                round(duration, 2),
                round(overdue, 2),
                log.notes
            ])
        
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=status_logs_{datetime.now().strftime("%Y%m%d")}.xlsx'
        wb.save(response)
        return response
    export_to_excel.short_description = 'Export selected to Excel'
