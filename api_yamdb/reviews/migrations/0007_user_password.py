# Generated by Django 3.2 on 2023-07-22 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_remove_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1, max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
