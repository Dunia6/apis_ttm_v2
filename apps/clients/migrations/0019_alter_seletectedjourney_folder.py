# Generated by Django 3.2.9 on 2022-10-08 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0018_auto_20220731_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seletectedjourney',
            name='folder',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='clients.journeyclientfolder', verbose_name='folder'),
        ),
    ]
