# Generated by Django 4.2.1 on 2024-02-21 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0011_alter_category_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='item_type', to='market.itemtype'),
        ),
    ]
