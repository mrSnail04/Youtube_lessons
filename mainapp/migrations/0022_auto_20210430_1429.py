# Generated by Django 3.2 on 2021-04-30 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0021_auto_20210430_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='buying_type',
            field=models.CharField(choices=[('self', 'Самовывоз'), ('delivery', 'Доставка')], default='self', max_length=100, verbose_name='Тип заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Новый заказ'), ('completed', 'Заказ выполнен'), ('is_ready', 'Заказ готов'), ('in_progress', 'Заказ в обработке')], default='new', max_length=100, verbose_name='Статус заказа'),
        ),
    ]
