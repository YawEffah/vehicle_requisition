# Generated by Django 5.0.7 on 2024-08-13 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carrequest',
            name='descritpion',
            field=models.TextField(default='For funeral', max_length=500),
            preserve_default=False,
        ),
    ]