# Generated by Django 3.2.9 on 2021-11-20 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0004_self'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='identity',
            field=models.CharField(default=0, max_length=32),
            preserve_default=False,
        ),
    ]
