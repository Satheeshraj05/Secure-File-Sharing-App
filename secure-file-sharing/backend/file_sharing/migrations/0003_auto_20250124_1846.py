# Generated by Django 3.2.10 on 2025-01-24 18:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import file_sharing.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('file_sharing', '0002_auto_20250123_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='encrypted_key',
            field=models.BinaryField(default=file_sharing.models.generate_key),
        ),
        migrations.AddField(
            model_name='file',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='fileshare',
            name='expiration',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fileshare',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_sharing.file'),
        ),
        migrations.AlterField(
            model_name='fileshare',
            name='permission',
            field=models.CharField(choices=[('view', 'View'), ('download', 'Download')], max_length=10),
        ),
        migrations.AlterField(
            model_name='fileshare',
            name='shared_with',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shareablelink',
            name='expiration',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='shareablelink',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='file_sharing.file'),
        ),
    ]
