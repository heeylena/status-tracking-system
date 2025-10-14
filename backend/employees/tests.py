"""
Tests for Employee Status Tracking System.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Employee, Status, StatusLog


class EmployeeModelTest(TestCase):
    """Test Employee model."""
    
    def setUp(self):
        self.employee = Employee.objects.create(
            name='Test Employee',
            email='test@example.com'
        )
    
    def test_employee_creation(self):
        """Test employee is created correctly."""
        self.assertEqual(self.employee.name, 'Test Employee')
        self.assertEqual(self.employee.email, 'test@example.com')
        self.assertTrue(self.employee.is_active)
    
    def test_soft_delete(self):
        """Test employee soft delete."""
        self.employee.soft_delete()
        self.assertFalse(self.employee.is_active)
        self.assertIsNotNone(self.employee.deleted_at)


class StatusLogModelTest(TestCase):
    """Test StatusLog model and business logic."""
    
    def setUp(self):
        self.employee = Employee.objects.create(name='Test Employee')
        self.status = Status.objects.create(
            name='Test Status',
            color='#3b82f6',
            has_end_time=True
        )
        self.user = User.objects.create_user(username='admin', password='test123')
    
    def test_status_log_creation(self):
        """Test status log is created correctly."""
        log = StatusLog.objects.create(
            employee=self.employee,
            status=self.status,
            created_by=self.user
        )
        self.assertEqual(log.employee, self.employee)
        self.assertEqual(log.status, self.status)
        self.assertIsNone(log.end_time)
    
    def test_elapsed_time_calculation(self):
        """Test elapsed time calculation."""
        log = StatusLog.objects.create(
            employee=self.employee,
            status=self.status
        )
        # Wait a moment
        import time
        time.sleep(1)
        elapsed = log.get_elapsed_seconds()
        self.assertGreaterEqual(elapsed, 1)
    
    def test_overdue_calculation(self):
        """Test overdue detection and calculation."""
        # Create log with planned end time in the past
        past_time = timezone.now() - timedelta(hours=2)
        log = StatusLog.objects.create(
            employee=self.employee,
            status=self.status,
            planned_end_time=past_time
        )
        
        self.assertTrue(log.is_overdue())
        overdue_seconds = log.get_overdue_seconds()
        self.assertGreater(overdue_seconds, 0)
    
    def test_overdue_duration_on_close(self):
        """Test overdue duration is calculated when closing a log."""
        past_time = timezone.now() - timedelta(hours=1)
        log = StatusLog.objects.create(
            employee=self.employee,
            status=self.status,
            planned_end_time=past_time
        )
        
        # Close the log
        log.end_time = timezone.now()
        log.calculate_and_save_overdue_duration()
        
        self.assertGreater(log.overdue_duration, 0)


class EmployeeAPITest(APITestCase):
    """Test Employee API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='test123')
        self.client.force_authenticate(user=self.user)
        
        self.employee = Employee.objects.create(name='Test Employee')
        self.status = Status.objects.create(
            name='Ready',
            color='#22c55e',
            has_end_time=False
        )
        StatusLog.objects.create(
            employee=self.employee,
            status=self.status
        )
    
    def test_get_employee_list(self):
        """Test getting employee list."""
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIsNotNone(response.data[0]['current_status'])
    
    def test_change_employee_status(self):
        """Test changing employee status."""
        new_status = Status.objects.create(
            name='Vacation',
            color='#f7b500',
            has_end_time=True
        )
        
        future_time = timezone.now() + timedelta(days=7)
        response = self.client.post(
            f'/api/employees/{self.employee.id}/change-status/',
            {
                'status_id': new_status.id,
                'planned_end_time': future_time.isoformat(),
                'notes': 'Going on vacation'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that old log was closed
        old_log = StatusLog.objects.get(employee=self.employee, status=self.status)
        self.assertIsNotNone(old_log.end_time)
        
        # Check that new log was created
        new_log = self.employee.get_current_status_log()
        self.assertEqual(new_log.status, new_status)
        self.assertEqual(new_log.notes, 'Going on vacation')
    
    def test_get_employee_history(self):
        """Test getting employee status history."""
        response = self.client.get(f'/api/employees/{self.employee.id}/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_unauthorized_access(self):
        """Test that unauthenticated requests are rejected."""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticationAPITest(APITestCase):
    """Test authentication endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='test123')
    
    def test_login(self):
        """Test login endpoint."""
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'admin', 'password': 'test123'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        response = self.client.post(
            '/api/auth/login/',
            {'username': 'admin', 'password': 'wrongpassword'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
