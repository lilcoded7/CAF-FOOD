# Generated by Django 4.2.4 on 2023-09-14 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CAFFOOD', '0007_food_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkingDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='food',
            name='days',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='CAFFOOD.workingdays'),
        ),
    ]
