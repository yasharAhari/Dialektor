# Generated by Django 3.0.3 on 2020-02-28 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dialektor', '0007_auto_20200218_1811'),
    ]

    operations = [
        migrations.RenameField(
            model_name='collection',
            old_name='owner',
            new_name='user_id',
        ),
    ]