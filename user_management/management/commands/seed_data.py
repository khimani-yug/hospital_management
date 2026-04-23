from django.core.management.base import BaseCommand
from user_management.models import Role, Department

class Command(BaseCommand):
    help = 'Seeds the database with initial roles and departments'

    def handle(self, *args, **kwargs):
        roles = ['Admin', 'Doctor', 'Receptionist', 'Patient']
        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created role: {role_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Role already exists: {role_name}'))

        departments = ['Cardiology', 'Neurology', 'Orthopedics', 'General Medicine']
        for dept_name in departments:
            dept, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created department: {dept_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Department already exists: {dept_name}'))
