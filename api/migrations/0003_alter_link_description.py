# Generated by Django 5.1.3 on 2024-11-11 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_link_image_link_type_link_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
