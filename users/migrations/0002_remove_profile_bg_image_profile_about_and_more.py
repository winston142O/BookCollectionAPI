# Generated by Django 4.2.7 on 2023-12-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="bg_image",
        ),
        migrations.AddField(
            model_name="profile",
            name="about",
            field=models.CharField(blank=True, max_length=600),
        ),
        migrations.AddField(
            model_name="profile",
            name="address",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="profile",
            name="phone",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]