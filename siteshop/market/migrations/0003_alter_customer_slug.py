# Generated by Django 4.2.1 on 2024-02-15 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_alter_customer_options_customer_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]