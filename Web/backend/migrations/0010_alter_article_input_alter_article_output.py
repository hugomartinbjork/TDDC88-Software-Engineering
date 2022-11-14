# Generated by Django 4.1.1 on 2022-11-14 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_alter_order_order_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='input',
            field=models.CharField(choices=[('ml', 'Millilitres'), ('cl', 'Centilitres'), ('dl', 'Decilitres'), ('l', 'Litres'), ('mm', 'Millimetres'), ('cm', 'Centimetres'), ('m', 'Metres'), ('pieces', 'Pieces'), ('crates', 'Crates'), ('bottles', 'Bottles')], default='ml', max_length=100),
        ),
        migrations.AlterField(
            model_name='article',
            name='output',
            field=models.CharField(choices=[('ml', 'Millilitres'), ('cl', 'Centilitres'), ('dl', 'Decilitres'), ('l', 'Litres'), ('mm', 'Millimetres'), ('cm', 'Centimetres'), ('m', 'Metres'), ('pieces', 'Pieces'), ('crates', 'Crates'), ('bottles', 'Bottles')], default='ml', max_length=100),
        ),
    ]
