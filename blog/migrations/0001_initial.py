# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 21:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('slug', models.SlugField(max_length=40, unique=True)),
                ('accent_image', models.ImageField(upload_to='categories')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(height_field='image_height', upload_to='%Y/%m/%d', width_field='image_width')),
                ('image_width', models.IntegerField()),
                ('image_height', models.IntegerField()),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'images',
                'ordering': ['-upload_date'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(blank=True, null=True)),
                ('text', models.TextField(help_text='Use the following notation to attach a picture. ![PictureName][] Make sure the picture name matches a value in the "Chosen Images" below.')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=False, help_text="Tick to make this entry live (see also the publication date). Note that administrators (like yourself) are allowed to preview inactive entries whereas the general public aren't.")),
                ('published_date', models.DateTimeField(blank=True, help_text='For an entry to be published, it must be active and its publication date must be in the past.', null=True, verbose_name='Publication date')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('header_image', models.ImageField(upload_to='%Y/%m/%d')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category')),
                ('images', models.ManyToManyField(blank=True, to='blog.Image')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sites.Site')),
            ],
            options={
                'verbose_name_plural': 'posts',
                'ordering': ['-published_date'],
                'get_latest_by': 'published_date',
            },
        ),
    ]
