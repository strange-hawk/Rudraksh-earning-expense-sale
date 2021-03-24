# Generated by Django 3.1.7 on 2021-03-22 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=100)),
                ('reference', models.CharField(max_length=255)),
                ('contact', models.CharField(max_length=10)),
            ],
        ),
    ]