"""
Celery tasks for Employee Status Tracking System.
"""
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import StatusLog, Employee


@shared_task
def generate_daily_report():
    """
    Generate daily report of overdue employees.
    Sends email to admin with employees currently overdue.
    """
    overdue_logs = StatusLog.objects.filter(
        end_time__isnull=True,
        planned_end_time__isnull=False,
        planned_end_time__lt=timezone.now()
    ).select_related('employee', 'status')
    
    if not overdue_logs.exists():
        return "No overdue statuses found."
    
    # Build email content
    message_lines = ["Daily Overdue Status Report\n" + "=" * 50 + "\n"]
    
    for log in overdue_logs:
        overdue_seconds = log.get_overdue_seconds()
        overdue_hours = overdue_seconds / 3600
        
        message_lines.append(
            f"Employee: {log.employee.name}\n"
            f"Status: {log.status.name}\n"
            f"Started: {log.start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Planned End: {log.planned_end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Overdue: {overdue_hours:.2f} hours\n"
            f"{'-' * 50}\n"
        )
    
    message = "\n".join(message_lines)
    
    # Send email (configure EMAIL_* settings in settings.py)
    try:
        send_mail(
            subject='Daily Overdue Status Report',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return f"Report sent with {overdue_logs.count()} overdue statuses."
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def check_overdue_statuses():
    """
    Check for statuses approaching deadline and send alerts.
    Runs every hour to notify about statuses that will be overdue soon.
    """
    from datetime import timedelta
    
    # Find statuses ending in the next 2 hours
    warning_time = timezone.now() + timedelta(hours=2)
    
    upcoming_logs = StatusLog.objects.filter(
        end_time__isnull=True,
        planned_end_time__isnull=False,
        planned_end_time__lte=warning_time,
        planned_end_time__gt=timezone.now()
    ).select_related('employee', 'status')
    
    if not upcoming_logs.exists():
        return "No statuses approaching deadline."
    
    # Build notification
    message_lines = ["Upcoming Deadline Alert\n" + "=" * 50 + "\n"]
    
    for log in upcoming_logs:
        remaining_seconds = log.get_remaining_seconds()
        remaining_hours = remaining_seconds / 3600 if remaining_seconds else 0
        
        message_lines.append(
            f"Employee: {log.employee.name}\n"
            f"Status: {log.status.name}\n"
            f"Planned End: {log.planned_end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Time Remaining: {remaining_hours:.2f} hours\n"
            f"{'-' * 50}\n"
        )
    
    message = "\n".join(message_lines)
    
    try:
        send_mail(
            subject='Status Deadline Alert',
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
        return f"Alert sent for {upcoming_logs.count()} upcoming deadlines."
    except Exception as e:
        return f"Failed to send alert: {str(e)}"


@shared_task
def cleanup_old_logs():
    """
    Archive or cleanup old status logs.
    This task can be customized based on retention requirements.
    """
    from datetime import timedelta
    
    # Example: Delete logs older than 2 years (adjust as needed)
    cutoff_date = timezone.now() - timedelta(days=730)
    
    old_logs = StatusLog.objects.filter(start_time__lt=cutoff_date)
    count = old_logs.count()
    
    # Instead of deleting, you might want to archive to another table
    # For now, we'll just count them
    # old_logs.delete()
    
    return f"Found {count} logs older than 2 years (not deleted, just counted)."
