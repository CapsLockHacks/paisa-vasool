# Generated by Django 2.2.6 on 2019-10-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upi', '0003_payment_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=5, unique=True),
        ),
    ]
