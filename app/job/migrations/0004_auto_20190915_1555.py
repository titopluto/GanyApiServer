# Generated by Django 2.2.4 on 2019-09-15 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('job', '0003_auto_20190830_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='job',
            name='assignor',
        ),
        migrations.AddField(
            model_name='job',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='job',
            name='executor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='executor', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
