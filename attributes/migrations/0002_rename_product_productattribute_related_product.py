# Generated by Django 4.1.7 on 2023-04-03 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productattribute',
            old_name='product',
            new_name='related_product',
        ),
    ]
