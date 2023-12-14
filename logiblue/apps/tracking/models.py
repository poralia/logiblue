from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.URLField()
    currency = models.CharField(max_length=5)
    iso_code = models.CharField(max_length=5)

    class Meta:
        verbose_name_plural = _("Countries")

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    country = models.ForeignKey(
        'tracking.Country',
        related_name='categories',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    price_per_kilo = models.FloatField()

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self) -> str:
        return self.title
