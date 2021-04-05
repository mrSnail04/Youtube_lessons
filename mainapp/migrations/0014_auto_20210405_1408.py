# Generated by Django 3.1.6 on 2021-04-05 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0013_auto_20210405_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('is_ready', 'Заказ готов'), ('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('completed', 'Заказ выполнен')], default='new', max_length=100, verbose_name='Статус заказа'),
        ),
    ]
