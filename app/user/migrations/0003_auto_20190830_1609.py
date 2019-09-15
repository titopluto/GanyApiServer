# Generated by Django 2.2.4 on 2019-08-30 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_is_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, help_text='Designates whether the user                                     can log into this admin site.', verbose_name='admin status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user is                                     a department staff', verbose_name='staff status'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates whether the user                                         is a superuser', verbose_name='superuser status'),
        ),
    ]
