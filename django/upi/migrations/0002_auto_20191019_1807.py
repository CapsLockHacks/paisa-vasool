# Generated by Django 2.2.6 on 2019-10-19 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='last_payment_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='upi.Payment'),
        ),
    ]
