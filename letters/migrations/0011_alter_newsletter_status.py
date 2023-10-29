# Generated by Django 4.2.5 on 2023-10-29 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0010_client_owner_message_owner_newsletter_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена'), ('off', 'Отключена')], default='Создана', max_length=10, verbose_name='Статус'),
        ),
    ]
