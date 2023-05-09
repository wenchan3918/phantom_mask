from django.db import models


# Create your models here.

class ENWord(models.Model):
    class Meta:
        verbose_name = '全英文單字庫'
        verbose_name_plural = '全英文單字庫'

    en = models.CharField(verbose_name="英文單字/片語",
                          max_length=64,
                          unique=True)

    zh = models.CharField(verbose_name="中文翻譯",
                          max_length=32,
                          blank=True,
                          null=True)

    is_toeic = models.BooleanField(verbose_name="多益庫",
                                   default=False)

    is_phrase = models.BooleanField(verbose_name="片語類型",
                                    default=False)

    def __str__(self):
        return self.en
