import pkg_resources
from django.core.management import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Load all fixtures for the project'

    def handle(self, *args, **kwargs):
        fixtures = [
            'fixtures/auth_user.json',
            'fixtures/contract_statuses.json',
            'fixtures/countries.json',
            'fixtures/plans.json',
            'fixtures/state_provinces.json',
            'fixtures/supported_languages.json',
            'fixtures/timezones.json',
            'fixtures/user_types.json',
            'fixtures/user_profiles.json',
            'fixtures/tenants.json',
        ]

        for fixture in fixtures:
            try:
                fixture_path = pkg_resources.resource_filename('buzzerboy_saas_tenants', fixture)
                call_command('loaddata', fixture_path)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded: {fixture_path}'))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error loading fixture {fixture}: {e}"))

