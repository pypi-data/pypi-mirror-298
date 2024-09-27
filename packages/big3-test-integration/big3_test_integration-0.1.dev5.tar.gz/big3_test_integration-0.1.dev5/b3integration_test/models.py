from enum import Enum

from django.db import models

from b3integrations.models import AbstractIntegrationModel
from b3integrations.models import AbstractSettingsSingleton


class SettingsTestIntegration(AbstractSettingsSingleton):
    name_1 = models.CharField(max_length=1000, null=True, blank=True)
    name_2 = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return '<<App settings "b3integration_test">>'


class BuildingTest(AbstractIntegrationModel):
    square = models.FloatField(null=True, blank=True)
    owner_name = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Дом (тест)'
        verbose_name_plural = 'Дома (тест)'
        abstract = False


class CommercialTest(AbstractIntegrationModel):
    square = models.FloatField(null=True, blank=True)
    owner_name = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Коммерческие помещения (тест)'
        verbose_name_plural = 'Коммерческие помещения (тест)'
        abstract = False
