# Generated by Django 3.1.6 on 2021-03-06 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20210306_1237'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='products',
        ),
    ]
