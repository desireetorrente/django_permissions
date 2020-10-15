class BotxoPermissionsMixin:

    def grant_permissions(self, user):
        model_class = self.user__class__.__name__.lower()
        if user.has_perm(f'learning.view_{model_class}'):
            read_permissions = Group.objects.get(name=f"{self.username}: Read")
            user.groups.add(read_permissions)

        if user.has_perm(f'learning.change_{model_class}') and \
                user.has_perm(f'learning.delete_{model_class}'):
            write_permissions = Group.objects.get(name=f"{self.username}: Write")
            user.groups.add(write_permissions)

        if user.has_perm(f'learning.change_{model_class}') and \
                not user.has_perm(f'learning.delete_{model_class}'):
            own_permissions = Group.objects.get(name=f"{self.username}: Own")
            user.groups.add(own_permissions)
