# Generated by Django 2.1.7 on 2019-03-25 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorprofile',
            name='nickname',
            field=models.CharField(blank=True, max_length=20, verbose_name='Kaldenavn'),
        ),
    ]
