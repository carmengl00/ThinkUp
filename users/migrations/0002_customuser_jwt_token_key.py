# Generated by Django 4.2.3 on 2023-11-03 10:09

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='jwt_token_key',
            field=models.CharField(default=users.models.generate_jwt_token, max_length=12),
        ),
    ]
