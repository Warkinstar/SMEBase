from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.core.validators import RegexValidator


BIN_IIN_REGEX = "^\d{12}$"


class BaseModel(models.Model):
    """Базовая модель"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class OwnershipType(BaseModel):
    """Тип собственности бизнеса"""

    name = models.CharField("Название формы собственности", max_length=255)
    description = models.TextField("Описание формы собственности", blank=True)

    def __str__(self):
        return self.name


class BusinessType(BaseModel):
    """Тип бизнеса"""

    name = models.CharField("Название типа бизнеса", max_length=255)
    description = models.TextField("Описание типа бизнеса", blank=True)

    def __str__(self):
        return self.name


class Company(BaseModel):
    """Модель для хранения информации о компании"""

    name = models.CharField(
        "Название компании",
        max_length=200,
        unique=True,
        help_text="Название бизнеса должно быть уникальным, которое не используется другими компаниями в вашей юрисдикции.",
    )

    # user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    # БИН & ИИН
    tax_id = models.CharField(
        "Введите ИИН или БИН",
        max_length=12,
        validators=[RegexValidator(regex=BIN_IIN_REGEX, message="Введите 12-й номер")],
        unique=True,
        help_text="Введите ИИН если вы индивидуальный предприниматель, БИН в другом случае",
    )

    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # форма собственности
    ownership_type = models.ForeignKey(
        OwnershipType,
        on_delete=models.PROTECT,
        verbose_name="Форма собственности",
        help_text="Выберите форму собственности, которой принадлежит компания",
    )
    # тип бизнеса
    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.PROTECT,
        verbose_name="Тип бизнеса",
        help_text="Выберите тип бизнеса, которым занимается компания.",
    )
    # рабочии

    description = models.TextField(
        "Описание деятельности компании", blank=True, help_text="Необязательно"
    )
    address = models.CharField("Адрес компании", max_length=200)
    phone_number = PhoneNumberField("Номер телефона компании", region="KZ")
    email = models.EmailField("Электронный адрес компании")
    website = models.URLField(
        "Веб-сайт компании", blank=True, help_text="Необязательно"
    )
    # Фото, логотип ImageField

    class Meta:
        verbose_name_plural = "Enterprises"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)
