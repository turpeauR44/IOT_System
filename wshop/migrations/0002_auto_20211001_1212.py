# Generated by Django 3.2.7 on 2021-10-01 10:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wshop', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProdLine_Specific_Values',
            new_name='ProdLine_Specific_Value',
        ),
        migrations.RenameField(
            model_name='prodline_specific_value',
            old_name='specif',
            new_name='specifvalue',
        ),
    ]
