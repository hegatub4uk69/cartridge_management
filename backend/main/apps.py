from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_initial_departments(sender, **kwargs):
    Department = sender.get_model('Department')
    default_departments = ["Необходима заправка", "Заправка", "Списан"]

    for name in default_departments:
        Department.objects.get_or_create(name=name)

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        post_migrate.connect(create_initial_departments, sender=self)