# Generated by Django 3.2.9 on 2021-11-20 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('node', '0005_company_identity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='productImage',
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
    ]
