# Generated by Django 3.2.9 on 2021-11-20 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ip',
            field=models.CharField(default='0.0.0.0', max_length=100),
            preserve_default=False,
        ),
    ]
