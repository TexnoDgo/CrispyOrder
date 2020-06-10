from django.db import models


class HomePageFile(models.Model):
    ImageFile = models.ImageField(verbose_name='Картинки', null=True, upload_to='SiteImage')
    heading = models.CharField(max_length=240, null=True)
    description = models.TextField(null=True)


class CADFile(models.Model):
    file = models.FileField(upload_to='otherFiles')
