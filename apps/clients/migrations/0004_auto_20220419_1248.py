# Generated by Django 3.2.9 on 2022-04-19 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_rename_dateexpiration_journeysession_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otherinforeservation',
            name='adress_from',
            field=models.CharField(max_length=250, verbose_name='adress_from'),
        ),
        migrations.AlterField(
            model_name='otherinforeservation',
            name='adress_to',
            field=models.CharField(max_length=250, verbose_name='adress_to'),
        ),
        migrations.AlterField(
            model_name='otherinforeservation',
            name='email',
            field=models.EmailField(max_length=200, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='otherinforeservation',
            name='num_piece_id',
            field=models.CharField(max_length=200, verbose_name='num_piece_id'),
        ),
        migrations.AlterField(
            model_name='otherinforeservation',
            name='num_tel',
            field=models.CharField(max_length=200, verbose_name='num_tel'),
        ),
        migrations.AlterField(
            model_name='otherinforeservation',
            name='num_tel_emergency',
            field=models.CharField(max_length=200, verbose_name='num_tel_emergency'),
        ),
        migrations.AlterField(
            model_name='otherinforeservation',
            name='piece_id',
            field=models.CharField(max_length=200, verbose_name='piece_id'),
        ),
    ]
