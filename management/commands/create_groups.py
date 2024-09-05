from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create initial groups and permissions'

    def handle(self, *args, **kwargs):
        # Criação do grupo SuperUser
        superuser_group, created = Group.objects.get_or_create(name='SuperUser')

        # Adicionar todas as permissões ao SuperUser
        all_permissions = Permission.objects.all()
        superuser_group.permissions.set(all_permissions)

        # Criação do grupo para usuários com permissões limitadas
        limited_group, created = Group.objects.get_or_create(name='LimitedUser')

        self.stdout.write(self.style.SUCCESS('Grupos e permissões criados com sucesso!'))
