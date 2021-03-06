# Generated by Django 2.2.5 on 2020-08-18 01:29

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('talks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spit',
            name='userid',
        ),
        migrations.AddField(
            model_name='spit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='spit',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(default=''),
        ),
        migrations.AlterField(
            model_name='spit',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='spits', to='talks.Spit'),
        ),
    ]
