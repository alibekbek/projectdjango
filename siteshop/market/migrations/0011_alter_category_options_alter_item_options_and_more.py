# Generated by Django 4.2.1 on 2024-02-21 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0010_item_itemtype_price_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория заказчика', 'verbose_name_plural': 'Категории заказчиков'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='itemtype',
            options={'verbose_name': 'Категория товара', 'verbose_name_plural': 'Категории товаров'},
        ),
        migrations.AddField(
            model_name='price',
            name='item',
            field=models.ForeignKey(default=1000, on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='market.item'),
            preserve_default=False,
        ),
    ]
