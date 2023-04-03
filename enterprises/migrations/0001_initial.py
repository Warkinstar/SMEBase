# Generated by Django 4.1.7 on 2023-04-03 11:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BusinessType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Название типа бизнеса"
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Описание типа бизнеса"),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OwnershipType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Название формы собственности"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, verbose_name="Описание формы собственности"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        help_text="Название бизнеса должно быть уникальным, которое не используется другими компаниями в вашей юрисдикции.",
                        max_length=200,
                        unique=True,
                        verbose_name="Название компании",
                    ),
                ),
                (
                    "tax_id",
                    models.CharField(
                        help_text="Введите ИИН если вы индивидуальный предприниматель, БИН в другом случае",
                        max_length=12,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введите 12-й номер", regex="^\\d{12}$"
                            )
                        ],
                        verbose_name="Введите ИИН или БИН",
                    ),
                ),
                ("slug", models.SlugField(blank=True, max_length=200, unique=True)),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Необязательно",
                        verbose_name="Описание деятельности компании",
                    ),
                ),
                (
                    "address",
                    models.CharField(max_length=200, verbose_name="Адрес компании"),
                ),
                (
                    "phone_number",
                    phonenumber_field.modelfields.PhoneNumberField(
                        max_length=128,
                        region="KZ",
                        verbose_name="Номер телефона компании",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, verbose_name="Электронный адрес компании"
                    ),
                ),
                (
                    "website",
                    models.URLField(
                        blank=True,
                        help_text="Необязательно",
                        verbose_name="Веб-сайт компании",
                    ),
                ),
                (
                    "business_type",
                    models.ForeignKey(
                        help_text="Выберите тип бизнеса, которым занимается компания.",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="enterprises.businesstype",
                        verbose_name="Тип бизнеса",
                    ),
                ),
                (
                    "ownership_type",
                    models.ForeignKey(
                        help_text="Выберите форму собственности, которой принадлежит компания",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="enterprises.ownershiptype",
                        verbose_name="Форма собственности",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Enterprises",
            },
        ),
    ]
