# Generated by Django 5.1.6 on 2025-03-10 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0035_beneficiaryregister_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='beneficiaryregister',
            name='C_Pass',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopowner',
            name='C_S_Pass',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
