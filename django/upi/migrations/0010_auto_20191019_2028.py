# Generated by Django 2.2.6 on 2019-10-19 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upi', '0009_contact_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]