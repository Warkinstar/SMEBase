# Generated by Django 4.1.7 on 2023-04-09 08:33

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="middle_name",
            field=models.CharField(blank=True, max_length=30, verbose_name="отчество"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                max_length=128, null=True, region="KZ", verbose_name="номер телефона"
            ),
        ),
    ]
