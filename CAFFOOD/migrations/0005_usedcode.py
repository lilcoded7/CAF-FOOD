# Generated by Django 4.2.4 on 2023-09-04 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CAFFOOD', '0004_order_order_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
