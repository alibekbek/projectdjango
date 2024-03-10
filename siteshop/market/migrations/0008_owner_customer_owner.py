# Generated by Django 4.2.1 on 2024-02-16 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_tagpost_alter_customer_cat_customer_tags'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('iin', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='owner',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='market.owner'),
        ),
    ]