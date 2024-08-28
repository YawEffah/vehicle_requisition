# Generated by Django 5.0.7 on 2024-08-16 01:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0007_vehicle_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrequest',
            name='vehicle',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='requisition.vehicle'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='picture',
            field=models.ImageField(default=1, upload_to='vehicle_pictures/'),
            preserve_default=False,
        ),
    ]
