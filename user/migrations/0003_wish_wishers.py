# Generated by Django 3.2.9 on 2021-12-05 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211205_0230'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='wishers',
            field=models.ManyToManyField(related_name='items', to='user.User'),
        ),
    ]