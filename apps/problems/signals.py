from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .services import seed_initial_content


@receiver(post_migrate)
def seed_problem_content(sender, **kwargs):
    if sender.name == "apps.problems":
        seed_initial_content()
