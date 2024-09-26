import uuid

from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('b3integration_test', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='settingstestintegration',
            name='name_1',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='settingstestintegration',
            name='name_2',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='settingstestintegration',
            name='password',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
