# Generated by Django 2.2.4 on 2021-04-12 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('combat_app', '0017_auto_20210402_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechniqueMods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q_power', models.DecimalField(decimal_places=2, max_digits=2)),
                ('q_speed', models.DecimalField(decimal_places=2, max_digits=2)),
                ('q_attack', models.DecimalField(decimal_places=2, max_digits=2)),
                ('n_power', models.DecimalField(decimal_places=2, max_digits=2)),
                ('n_attack', models.DecimalField(decimal_places=2, max_digits=2)),
                ('s_power', models.DecimalField(decimal_places=2, max_digits=2)),
                ('s_speed', models.DecimalField(decimal_places=2, max_digits=2)),
                ('s_attack', models.DecimalField(decimal_places=2, max_digits=2)),
                ('d_speed', models.DecimalField(decimal_places=2, max_digits=2)),
                ('d_agility', models.DecimalField(decimal_places=2, max_digits=2)),
                ('d_defense', models.DecimalField(decimal_places=2, max_digits=2)),
                ('n_speed', models.DecimalField(decimal_places=2, max_digits=2)),
                ('n_agility', models.DecimalField(decimal_places=2, max_digits=2)),
                ('n_defense', models.DecimalField(decimal_places=2, max_digits=2)),
                ('c_speed', models.DecimalField(decimal_places=2, max_digits=2)),
                ('c_agility', models.DecimalField(decimal_places=2, max_digits=2)),
                ('c_defense', models.DecimalField(decimal_places=2, max_digits=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
