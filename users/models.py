from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from orders.models import Suggestion, OperationCategories


class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __unicode__(self):
        return str(self.stripe_id)


class Profile(models.Model):
    TIMING_CHOICE = (
        (_('Never'), _('0 hours')),
        (_('Each hour'), _('1 hour')),
        (_('Every 3 hours'), _('3 hours')),
        (_('Every 6 hours'), _('6 hours')),
        (_('Every 12 hours'), _('12 hours')),
        (_('Every 24 hours'), _('24 hours')),
    )

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    rating = models.PositiveIntegerField(default=0)

    # ----------------------------------------Уведомления------------------------------------------------
    # Получать уведомления о новых заказа в категории?
    notifications = models.BooleanField(default=False, verbose_name=_('Receive notifications?'))
    # Получать уведомления в личный аккаунт
    notifi_account = models.BooleanField(default=False, verbose_name=_('Notifications to the office?'))
    # Получать уведомления на эл. почту
    notifi_email = models.BooleanField(default=False, verbose_name=_('Email notifications?'))
    # Поулчать уведомления по смс
    notifi_sms = models.BooleanField(default=False, verbose_name=_('SMS notifications'))
    # Получать уведомлекния новостях сайта
    notifi_news = models.BooleanField(default=False, verbose_name=_('News?'))
    # Получать уведомления о Статьях на сайте
    notifi_articles = models.BooleanField(default=False, verbose_name=_('Articles?'))
    # Получать уведомления об обновлениях сайта.
    notifi_updates = models.BooleanField(default=False, verbose_name=_('Updates?'))
    # Частота обновления
    timing = models.CharField(max_length=30, choices=TIMING_CHOICE, default=_('Never'),
                              verbose_name=_('Update frequency'))
    # Категории уведомления
    categories = models.ManyToManyField(OperationCategories, blank=True, related_name='profile',
                                        verbose_name=_('Categories for notifications'))
    # -------------------------------------------Уведомления----------------------------------------------

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):  # Преобразование изображения
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class CompanyProfile(models.Model):
    user_name = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.TextField(verbose_name=_('Abbreviated company name'), default=_('CompanyName'))
    edrpou = models.CharField(max_length=10, verbose_name=_('EDRPOU'))
    officialName = models.TextField(verbose_name=_('The official name of the company'),
                                    default=_('OfficialCompanyName'))
    address = models.TextField(verbose_name=_('Company Registration Address'), default=_('CompanyAddress'))
    mainPerson = models.CharField(max_length=255, verbose_name=_('Head of the organization'),
                                  default=_('CompanyMainPerson'))
    occupation = models.TextField(verbose_name=_('The main activity of the organization'),
                                  default=_('CompanyOccupation'))
    status = models.CharField(max_length=255, verbose_name=_('Organization Status'), default=_('CompanyStatus'))

    def __str__(self):
        return self.name
