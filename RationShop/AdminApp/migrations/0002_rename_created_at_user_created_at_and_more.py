# Generated by Django 5.1.6 on 2025-02-10 06:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='Created_at',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='email',
            new_name='Email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='Mobile',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='Name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='Password',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='role',
            new_name='Role',
        ),
    ]
