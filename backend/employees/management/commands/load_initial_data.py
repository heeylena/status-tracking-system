"""
Management command to load initial data for the application.
"""
from django.core.management.base import BaseCommand
from employees.models import Status, Employee, StatusLog


class Command(BaseCommand):
    help = 'Load initial data for statuses and sample employees'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...\n')
        
        # Create default statuses
        statuses_data = [
            {'name': 'Ready', 'color': '#22c55e', 'has_end_time': False, 'display_order': 1},
            {'name': 'Repair', 'color': '#3b82f6', 'has_end_time': True, 'display_order': 2},
            {'name': 'Vacation', 'color': '#f7b500', 'has_end_time': True, 'display_order': 3},
            {'name': 'Sick Leave', 'color': '#ef4444', 'has_end_time': True, 'display_order': 4},
            {'name': 'Business Trip', 'color': '#8b5cf6', 'has_end_time': True, 'display_order': 5},
            {'name': 'Rest', 'color': '#6b7280', 'has_end_time': True, 'display_order': 6},
        ]
        
        created_statuses = 0
        for status_data in statuses_data:
            status, created = Status.objects.get_or_create(
                name=status_data['name'],
                defaults=status_data
            )
            if created:
                created_statuses += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created status: {status.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Status already exists: {status.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nCreated {created_statuses} new statuses.')
        )
        
        # Optionally create sample employees
        if self.confirm_action('Do you want to create sample employees? (yes/no): '):
            sample_employees = [
                {'name': 'John Smith', 'email': 'john.smith@example.com'},
                {'name': 'Maria Garcia', 'email': 'maria.garcia@example.com'},
                {'name': 'David Chen', 'email': 'david.chen@example.com'},
                {'name': 'Sarah Johnson', 'email': 'sarah.johnson@example.com'},
                {'name': 'Michael Brown', 'email': 'michael.brown@example.com'},
            ]
            
            created_employees = 0
            ready_status = Status.objects.get(name='Ready')
            
            for emp_data in sample_employees:
                employee, created = Employee.objects.get_or_create(
                    email=emp_data['email'],
                    defaults=emp_data
                )
                if created:
                    # Create initial status log
                    StatusLog.objects.create(
                        employee=employee,
                        status=ready_status
                    )
                    created_employees += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created employee: {employee.name}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'- Employee already exists: {employee.name}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS(f'\nCreated {created_employees} sample employees.')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\n✓ Initial data loading complete!')
        )
    
    def confirm_action(self, message):
        """Ask user for confirmation."""
        response = input(message)
        return response.lower() in ['yes', 'y']
