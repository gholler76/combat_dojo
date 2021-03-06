# Generated by Django 2.2.4 on 2021-04-12 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('combat_app', '0019_auto_20210411_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='techniquemod',
            old_name='c_agility',
            new_name='cd_agility',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='c_defense',
            new_name='cd_defense',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='c_speed',
            new_name='cd_speed',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='d_agility',
            new_name='dd_agility',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='d_defense',
            new_name='dd_defense',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='d_speed',
            new_name='dd_speed',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='n_agility',
            new_name='na_attack',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='n_attack',
            new_name='na_power',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='n_defense',
            new_name='na_speed',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='n_power',
            new_name='nd_agility',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='n_speed',
            new_name='nd_defense',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='q_attack',
            new_name='nd_speed',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='q_power',
            new_name='qa_attack',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='q_speed',
            new_name='qa_power',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='s_attack',
            new_name='qa_speed',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='s_power',
            new_name='sa_attack',
        ),
        migrations.RenameField(
            model_name='techniquemod',
            old_name='s_speed',
            new_name='sa_power',
        ),
        migrations.AddField(
            model_name='techniquemod',
            name='sa_speed',
            field=models.DecimalField(decimal_places=2, default=0.15, max_digits=2),
            preserve_default=False,
        ),
    ]
