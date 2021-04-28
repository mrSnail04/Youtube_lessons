# Generated by Django 3.2 on 2021-04-27 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0018_alter_order_status'),
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
            field=models.CharField(choices=[('is_ready', 'Заказ готов'), ('in_progress', 'Заказ в обработке'), ('completed', 'Заказ выполнен'), ('new', 'Новый заказ')], default='new', max_length=100, verbose_name='Статус заказа'),
        ),
    ]
