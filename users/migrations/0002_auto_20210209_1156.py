# Generated by Django 3.1.6 on 2021-02-09 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='metadata',
            field=models.JSONField(null=True),
        ),
    ]