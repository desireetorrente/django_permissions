from django.core.management.base import BaseCommand, CommandError
from learning.models import Company, User


class Command(BaseCommand):
    help = 'Create users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int)

    def handle(self, *args, **options):
        company = Company.objects.get(name='One')
        count = 0
        while count <= options['num_users']:
            try:
                user = User.objects.create(
                    username='user {}'.format(count),
                    password='admin1234.',
                    company=company,
                    role='AD')

                user.save()
                count += 1
            except Exception as e:
                raise CommandError('Usuario no creado {}'.format(e))

            self.stdout.write(self.style.SUCCESS('Usuario creado'))
