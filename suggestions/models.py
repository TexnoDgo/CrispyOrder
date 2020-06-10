from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from orders.models import CODOrder


class CODSuggestion(models.Model):
    SUGGESTION_STATUS = (
        (_('Discussion'), _('Discussion')),
        (_('InWork'), _('InWork')),
        (_('Done'), _('Done')),
        (_('Canceled'), _('Canceled')),
    )

    order = models.ForeignKey(CODOrder, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_create = models.DateTimeField(default=timezone.now)
    offer_description = models.TextField(verbose_name=_('Offer Description'))
    deadline = models.DateTimeField(verbose_name=_('Production time'))
    offer_price = models.PositiveIntegerField(verbose_name=_('Suggested price'))
    status = models.CharField(max_length=20, choices=SUGGESTION_STATUS, default=_('Discussion'),
                              verbose_name=_('Offer Status'))
    rating = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.offer_description


class CODFeedback(models.Model):
    suggestion = models.ForeignKey(CODSuggestion, on_delete=models.CASCADE)
    date_create = models.DateField(default=timezone.now)
    feet = models.TextField()

    def __str__(self):
        return self.feet
