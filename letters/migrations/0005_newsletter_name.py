# Generated by Django 4.2.5 on 2023-09-29 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0004_alter_maillog_last_sent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='name',
            field=models.CharField(default='Новая рассылка', max_length=255, verbose_name='Наименование'),
        ),
    ]
