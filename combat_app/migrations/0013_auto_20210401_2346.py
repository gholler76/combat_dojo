# Generated by Django 2.2.4 on 2021-04-02 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('combat_app', '0012_auto_20210401_2341'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fighterhealth',
            old_name='fighter1_health',
            new_name='fighter',
        ),
        migrations.RenameField(
            model_name='fighterhealth',
            old_name='fighter2_health',
            new_name='health',
        ),
    ]
