# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mftutor.gallery.utils
import datetime
import django.core.validators
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Titel', max_length=200)),
                ('publish_date', models.DateField(verbose_name='Udgivelsesdato', blank=True, null=True, default=datetime.date.today)),
                ('eventalbum', models.BooleanField(verbose_name='Arrangement', default=True)),
                ('gfyear', models.PositiveSmallIntegerField(verbose_name='Årgang', default=mftutor.gallery.utils.get_gfyear)),
                ('slug', models.SlugField(verbose_name='Kort titel')),
                ('description', models.TextField(verbose_name='Beskrivelse', blank=True)),
                ('oldFolder', models.CharField(max_length=200, blank=True)),
            ],
            options={
                'ordering': ['gfyear', '-eventalbum', 'oldFolder', 'publish_date'],
            },
        ),
        migrations.CreateModel(
            name='BaseMedia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('type', models.CharField(max_length=1, default='O', choices=[('I', 'Image'), ('V', 'Video'), ('A', 'Audio'), ('O', 'Other')])),
                ('date', models.DateTimeField(verbose_name='Dato', blank=True, null=True)),
                ('visibility', models.CharField(verbose_name='Synlighed', max_length=10, default='new', choices=[('public', 'Synligt'), ('discarded', 'Frasorteret'), ('sensitive', 'Skjult'), ('delete', 'Slet'), ('new', 'Ubesluttet')])),
                ('caption', models.CharField(verbose_name='Overskrift', max_length=200, blank=True)),
                ('slug', models.SlugField(verbose_name='Kort titel', blank=True, null=True)),
                ('forcedOrder', models.SmallIntegerField(verbose_name='Rækkefølge', default=0, validators=[django.core.validators.MinValueValidator(-10000), django.core.validators.MaxValueValidator(10000)])),
                ('isCoverFile', models.NullBooleanField(verbose_name='Vis på forsiden')),
            ],
            options={
                'ordering': ['forcedOrder', 'date', 'slug'],
                'select_on_save': True,
            },
        ),
        migrations.CreateModel(
            name='GenericFile',
            fields=[
                ('basemedia_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='gallery.BaseMedia')),
                ('originalFile', models.FileField(blank=True, upload_to=mftutor.gallery.utils.file_name)),
                ('file', models.FileField(upload_to=mftutor.gallery.utils.file_name)),
            ],
            options={
                'select_on_save': True,
            },
            bases=('gallery.basemedia',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('basemedia_ptr', models.OneToOneField(primary_key=True, serialize=False, auto_created=True, parent_link=True, to='gallery.BaseMedia')),
                ('file', versatileimagefield.fields.VersatileImageField(upload_to=mftutor.gallery.utils.file_name)),
            ],
            options={
                'select_on_save': True,
            },
            bases=('gallery.basemedia',),
        ),
        migrations.AddField(
            model_name='basemedia',
            name='album',
            field=models.ForeignKey(related_name='basemedia', to='gallery.Album'),
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('gfyear', 'slug')]),
        ),
        migrations.AlterUniqueTogether(
            name='basemedia',
            unique_together=set([('album', 'slug')]),
        ),
    ]
