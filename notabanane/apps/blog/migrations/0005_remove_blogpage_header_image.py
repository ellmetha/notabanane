# Generated by Django 2.1.7 on 2019-03-25 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20190324_2131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='header_image',
        ),
    ]
