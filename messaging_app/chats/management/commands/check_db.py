from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Check database connection and display database info'

    def handle(self, *args, **options):
        """Check database connection"""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                if result:
                    self.stdout.write(
                        self.style.SUCCESS('✓ Database connection successful')
                    )
                    
                    # Display database info
                    db_settings = connection.settings_dict
                    self.stdout.write(f"Database Engine: {db_settings['ENGINE']}")
                    self.stdout.write(f"Database Name: {db_settings['NAME']}")
                    self.stdout.write(f"Database Host: {db_settings.get('HOST', 'localhost')}")
                    self.stdout.write(f"Database Port: {db_settings.get('PORT', 'default')}")
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Database connection failed: {str(e)}')
            )
            raise
