from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='VOID',
                email='asad2001psabirov@gmail.com',
                password='2001'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser yaratildi'))
        else:
            self.stdout.write(self.style.WARNING('ℹ️ Superuser allaqachon mavjud'))
