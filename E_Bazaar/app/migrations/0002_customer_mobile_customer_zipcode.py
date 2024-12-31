# Generated by Django 5.1.3 on 2024-12-27 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='mobile',
            field=models.CharField(default='null=true', max_length=11),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='zipcode',
            field=models.IntegerField(null=True),
        ),
    ]
