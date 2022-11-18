from django.db import models


class Mask(models.Model):
    class Meta:
        verbose_name = 'Mask'
        verbose_name_plural = 'Mask'

    name = models.CharField(verbose_name='Name',
                            unique=True,
                            max_length=256, )

    def __str__(self):
        return self.name
