from django.core.management.base import BaseCommand
from apps.roles.models import Role

DEFAULT_ROLES = [
    ('ADMIN', 'System administrator'),
    ('HOD', 'Head of Department'),
    ('LECTURER', 'Lecturer'),
    ('DEAN', 'Dean'),
    ('EXAM_OFFICER', 'Exam officer'),
    ('STUDENT', 'Student'),
]


class Command(BaseCommand):
    help = 'Seed default roles into the database'

    def handle(self, *args, **options):
        created = 0
        for name, desc in DEFAULT_ROLES:
            obj, was_created = Role.objects.get_or_create(name=name, defaults={'description': desc})
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f'Created role: {name}'))
        if created == 0:
            self.stdout.write('No new roles created.')
        else:
            self.stdout.write(self.style.SUCCESS(f'Seeded {created} roles.'))
