from django.core.management.base import BaseCommand, CommandError
from learning.models import Bot, Company, User


class Command(BaseCommand):
    help = 'Create bots'

    def add_arguments(self, parser):
        parser.add_argument('num_bots', type=int)

    def handle(self, *args, **options):
        company = Company.objects.get(name='One')
        user = User.objects.get(username='desi')
        count = 0
        while count <= options['num_bots']:
            try:
                bot = Bot.objects.create(
                    name='bot{}'.format(count),
                    company=company,
                    created_by=user)

                bot.save()
                count += 1
            except Exception:
                raise CommandError('Bot no creado')

            self.stdout.write(self.style.SUCCESS('Bot creado'))
