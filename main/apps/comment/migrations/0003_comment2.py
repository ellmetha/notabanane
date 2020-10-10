# Generated by Django 3.1.1 on 2020-09-26 20:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comment', '0002_auto_20200426_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('unregistered_author_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email address')),
                ('unregistered_author_name', models.CharField(blank=True, max_length=30, null=True, verbose_name='Name')),
                ('unregistered_author_website_url', models.URLField(blank=True, null=True, verbose_name='Website')),
                ('notify_author', models.BooleanField(default=False, help_text='Define whether the author is notified when responses to the comment are made', verbose_name='Notify author')),
                ('content', models.TextField(validators=[django.core.validators.MaxLengthValidator(1000)], verbose_name='Content')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, unpack_ipv4=True, verbose_name='IP address')),
                ('commented_object_id', models.CharField(db_index=True, max_length=255)),
                ('commented_object_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='contenttypes.contenttype')),
                ('registered_author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='Poster')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'db_table': 'my_comments',
                'ordering': ('-created_at',),
            },
        ),
    ]
