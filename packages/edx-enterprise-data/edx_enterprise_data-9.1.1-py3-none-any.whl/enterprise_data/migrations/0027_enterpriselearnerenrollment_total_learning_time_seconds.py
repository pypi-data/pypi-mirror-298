# Generated by Django 3.2.12 on 2022-06-09 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprise_data', '0026_auto_20210916_0414'),
    ]

    operations = [
        migrations.AddField(
            model_name='enterpriselearnerenrollment',
            name='total_learning_time_seconds',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
