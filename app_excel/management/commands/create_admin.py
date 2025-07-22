from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **options):
        User = get_user_model()
        admin_username = 'admin'
        if User.objects.filter(username=admin_username).exists():
            User.objects.filter(username=admin_username).delete()
        User.objects.create_superuser(
            username=admin_username,
            email='admin@example.com',
            password='1'
        )
        self.stdout.write("✅ Admin foydalanuvchi yaratildi.")
