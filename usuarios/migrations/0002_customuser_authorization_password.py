# Generated by Django 5.0.7 on 2024-08-28 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='authorization_password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
