# Generated by Django 4.2.4 on 2023-09-02 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAFFOOD', '0003_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True),
        ),
    ]
