# Generated by Django 5.0.7 on 2024-08-16 16:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0009_alter_carrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrequest',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2024, 8, 16, 16, 5, 35, 35101, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]