# Generated by Django 3.2.3 on 2021-05-26 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_district_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district_data',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]