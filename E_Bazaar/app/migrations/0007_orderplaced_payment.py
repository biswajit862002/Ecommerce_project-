# Generated by Django 5.1.3 on 2025-01-02 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_orderplaced_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='payment',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='app.payment'),
        ),
    ]
