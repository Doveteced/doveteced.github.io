# Generated by Django 5.1.1 on 2024-10-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Advertisement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "main_image",
                    models.ImageField(upload_to="ads/main/", verbose_name="Main Image"),
                ),
                (
                    "image_2",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="ads/optional/",
                        verbose_name="Optional Image 2",
                    ),
                ),
                (
                    "image_3",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="ads/optional/",
                        verbose_name="Optional Image 3",
                    ),
                ),
                (
                    "url",
                    models.URLField(
                        help_text="URL where the ad redirects to when clicked",
                        max_length=255,
                        verbose_name="Link to Ad",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Advertisement",
                "verbose_name_plural": "Advertisements",
            },
        ),
        migrations.CreateModel(
            name="AdvertLeads",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(blank=True, max_length=15, null=True)),
                ("company", models.CharField(blank=True, max_length=100, null=True)),
                ("interest", models.CharField(blank=True, max_length=100, null=True)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Advert Lead",
                "verbose_name_plural": "Advert Leads",
            },
        ),
    ]
