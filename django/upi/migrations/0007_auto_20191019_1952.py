# Generated by Django 2.2.6 on 2019-10-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upi', '0006_auto_20191019_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=6, max_digits=18),
        ),
    ]