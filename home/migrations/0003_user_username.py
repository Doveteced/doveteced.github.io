# Generated by Django 5.1.4 on 2025-01-14 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_user_groups_user_is_superuser_user_user_permissions"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
