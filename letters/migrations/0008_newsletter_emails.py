# Generated by Django 4.2.5 on 2023-10-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0007_maillog_newsletter'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='emails',
            field=models.ManyToManyField(to='letters.client', verbose_name='Клиенты'),
        ),
    ]