# Generated by Django 3.2 on 2023-08-21 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0036_auto_20230821_1946'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_follow',
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')], default='user', max_length=256),
        ),
    ]
