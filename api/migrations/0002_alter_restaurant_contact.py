# Generated by Django 3.2.5 on 2021-07-23 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='contact',
            field=models.IntegerField(default=0),
        ),
    ]