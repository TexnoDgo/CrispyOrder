# Python
import stripe
# Django
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.conf import settings
# Apps
# ----
# Local
from .models import Profile, UserStripe

#stripe.api_key = settings.STRIPE_SECRET_KEY

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


'''def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email=str(user.email)
        )


def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        get_create_stripe(user)


post_save.connect(user_created, sender=User)'''