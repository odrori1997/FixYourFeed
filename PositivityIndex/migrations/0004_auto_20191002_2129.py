# Generated by Django 2.2.5 on 2019-10-03 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PositivityIndex', '0003_auto_20191002_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]