# Generated by Django 3.1.7 on 2021-03-23 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0004_auto_20210323_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='area',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
