# Generated by Django 4.0.6 on 2022-10-10 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_alter_user_birthday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.DateField(default='2022-10-10'),
        ),
    ]