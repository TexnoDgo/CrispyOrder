from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class CODCity(models.Model):
    title = models.CharField(max_length=50, default=_('not_selected'))

    objects = models.Manager()

    def __str__(self):
        return self.title


class CODMaterial(models.Model):
    title = models.CharField(max_length=250)

    objects = models.Manager()

    def __str__(self):
        return self.title


class CODCategories(models.Model):
    title = models.CharField(max_length=30)

    objects = models.Manager()

    def __str__(self):
        return self.title


class CODOrder(models.Model):
    BUDGET_EXAMPLE = (
        (_('Unknown'), _('Unknown')),
        (_('Small'), _('Small')),
        (_('Medium'), _('Medium')),
        (_('High'), _('High'))
    )

    ORDER_STATUS = (
        (_('Created'), _('Created')),
        (_('Discussion'), _('Discussion')),
        (_('InWork'), _('InWork')),
        (_('Done'), _('Done')),
        (_('Canceled'), _('Canceled')),
    )
    author = models.ForeignKey(User, on_delete=models.PROTECT)  # Автор заказа. Автоматически
    date_create = models.DateTimeField(default=timezone.now)  # Время создания заказа. Автоматически
    title = models.CharField(max_length=100, verbose_name=_('Headline'), default=_('Headline'))  # Заголовок заказа
    description = models.TextField(verbose_name=_('Description Order'),
                                   default=_('Description Order'))  # Описание заказа
    group_status = models.BooleanField(default=False, verbose_name=_('Group Status'))
    archive = models.FileField(upload_to='COD_order_archive',
                               verbose_name=_('Group Order Archive'), null=True)
    table = models.FileField(upload_to='COD_order_tables', null=True)
    pdf_cover = models.FileField(default='default.pdf', upload_to='COD_order_pdf_cover',
                                 verbose_name=_('Pdf order cover'))
    image_cover = models.ImageField(default='default.jpg', upload_to='COD_order_image_cover',
                                    verbose_name=_('Cover image'))
    Categories = models.ManyToManyField(CODCategories, blank=True, related_name='CODDetail',
                                        verbose_name=_('Categories'), default='Default')

    city = models.ForeignKey(CODCity, on_delete=models.PROTECT, verbose_name=_('Order City'),
                             null=True)  # Город заказа
    proposed_budget = models.CharField(max_length=40, choices=BUDGET_EXAMPLE, default=_('Unknown'),
                                       verbose_name=_('Budget'))  # Предложеный бюджет
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default=_('Created'),
                              verbose_name=_('Order status'))  # Статус заказ

    def __str__(self):
        return self.title
    
    def image_cover_url(self):
        if self.image_cover and hasattr(self.image_cover, 'url'):
            return self.image_cover.url


class CODDetail(models.Model):
    WHOSE = (
        (_('Author'), _('Author')),
        (_('Offeror'), _('Offeror')),
    )

    order = models.ForeignKey(CODOrder, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='Detail', verbose_name=_('Detail name'))
    amount = models.PositiveIntegerField(default=1, verbose_name=_('Number of products'))  # Кол-во изделий
    material = models.ForeignKey(CODMaterial, related_name=_('Material'),
                                      verbose_name=_('Materials'), on_delete=models.CASCADE, null=True)
    whose_material = models.CharField(max_length=10, choices=WHOSE, default=_('Offeror'),
                                      verbose_name=_('Whose material?'))
    Note = models.TextField(default=_('You Note'), verbose_name=_('You Note'))

    Deadline = models.DateField(verbose_name=_('Deadline'), null=True)
    Availability_date = models.DateField(verbose_name=_('Availability date'), null=True)
    image_cover = models.ImageField(default='COD_Detail_image_cover/default.jpg', upload_to='COD_Detail_image_cover',
                                    verbose_name=_('Cover image'))
    pdf = models.FileField(upload_to='COD_detail_files', blank=True, null=True, verbose_name=_('PDF'))
    dxf = models.FileField(upload_to='COD_detail_files', blank=True, null=True, verbose_name=_('DXF'))
    step = models.FileField(upload_to='COD_detail_files', blank=True, null=True, verbose_name=_('STEP'))
    part = models.FileField(upload_to='COD_detail_files', blank=True, null=True, verbose_name=_('PART'))


class CODFile(models.Model):
    file = models.FileField(upload_to='COD_detail_files', blank=True, null=True, verbose_name=_('File'))
    detail = models.ForeignKey(CODDetail, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('CODFiles')
        verbose_name_plural = _('CODFiles')

    def __str__(self):
        return self.file.name


class File(models.Model):
    file = models.FileField(upload_to='COD_detail_files', blank=True, null=True, verbose_name=_('File'))
    detail = models.ForeignKey(CODDetail, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Files')
        verbose_name_plural = _('Files')

    def __str__(self):
        return self.file.name
