# Generated by Django 5.1.6 on 2025-03-06 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0033_beneficiaryregister_shop_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopowner',
            name='District',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='Panchayat',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='Place',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='State',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='Taluk',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
