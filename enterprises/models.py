from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings
from django.core.validators import RegexValidator
from unidecode import unidecode
from django.utils import timezone


# Регулярно выражение для валидатора поля tax_id
BIN_IIN_REGEX = "^\d{12}$"  # Только 12 цифр
# Choices для пола
GENDER_CHOICES = [
    ("M", "Мужской"),
    ("F", "Женский"),
]


class BaseModel(models.Model):
    """Базовая абстрактная модель"""

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
        help_text="Название бизнеса должно быть уникальным и не использоваться другими компаниями в вашей юрисдикции.",
    )

    # user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="companies", on_delete=models.PROTECT
    )

    # БИН & ИИН
    tax_id = models.CharField(
        "Введите ИИН или БИН",
        max_length=12,
        validators=[RegexValidator(regex=BIN_IIN_REGEX, message="Введите 12-й номер")],
        unique=True,
        help_text="Введите ИИН если вы индивидуальный предприниматель, БИН в другом случае.",
    )

    slug = models.SlugField(max_length=200, unique=True, blank=True)

    # форма собственности
    ownership_type = models.ForeignKey(
        OwnershipType,
        on_delete=models.PROTECT,
        related_name="companies",
        verbose_name="Форма собственности",
        help_text="Выберите форму собственности, которой принадлежит компания.",
    )
    # тип бизнеса
    business_type = models.ForeignKey(
        BusinessType,
        on_delete=models.PROTECT,
        related_name="companies",
        verbose_name="Тип бизнеса",
        help_text="Выберите тип бизнеса, которым занимается компания.",
    )

    description = models.TextField(
        "Описание деятельности компании", blank=True, help_text="Необязательно."
    )
    address = models.CharField("Адрес компании", max_length=200)
    phone_number = PhoneNumberField("Номер телефона компании", region="KZ")
    email = models.EmailField("Электронный адрес компании")
    website = models.URLField(
        "Веб-сайт компании", blank=True, help_text="Необязательно."
    )
    # Фото, логотип компании
    image = models.ImageField(
        "Логотип или фото компании",
        upload_to="company_images/",
        blank=True,
        help_text="Необязательно",
    )

    class Meta:
        verbose_name_plural = "Enterprises"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("company_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # Если slug не установлен (первое создание объекта)
        if not self.slug:
            # slug
            self.slug = slugify(unidecode(self.name))
        return super().save(*args, **kwargs)


class Employee(BaseModel):
    """Модель для хранения информации о сотрудниках компании"""

    # Связь с компанией
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="employees"
    )

    # Информация о сотруднике
    first_name = models.CharField("Имя", max_length=255)
    last_name = models.CharField("Фамилия", max_length=255)
    middle_name = models.CharField(
        "Отчество", max_length=255, blank=True, help_text="Необязательно"
    )
    position = models.CharField("Должность", max_length=255)

    # Контактная информация
    email = models.EmailField("Электронный адрес")
    phone_number = PhoneNumberField("Номер телефона", region="KZ")

    # Доп. информация
    date_of_birth = models.DateField(
        "Дата рождения", blank=True, null=True, help_text="Необязательно"
    )

    image = models.ImageField(
        "Фото сотрудника",
        upload_to="employee_images/",
        blank=True,
        help_text="Необязательно",
    )

    gender = models.CharField(
        "Пол",
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        help_text="Необязательно",
    )

    def __str__(self):
        middle_name = f" {self.middle_name}" if self.middle_name else ""
        return f"{self.last_name} {self.first_name}" + middle_name


YEARS = [(year, year) for year in range(2000, timezone.now().year)]


class Financials(BaseModel):
    """Neutral and universal model for financial information about a company"""

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField(
        verbose_name="Отчет за год",
        choices=YEARS,
        help_text="За какой год информация ниже актуальна",
    )

    revenue = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Общая выручка",
        help_text="Показывает общую сумму денег, которую компания заработала за определенный год",
    )

    expenses = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Расходы",
        help_text="Поле может включать все расходы, связанные с бизнесом, такие как зарплата сотрудников, аренда помещения, закупка оборудования и т.д.",
    )

    gross_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Валовая прибыль",
        help_text="Это поле показывает разницу между выручкой и себестоимостью товаров или услуг.",
    )

    net_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Чистая прибыль",
        help_text="Это поле может показывать сумму денег, которую компания заработала после вычета всех расходов.",
    )

    taxes = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Налоги",
        help_text="Это поле может включать информацию о том, сколько налогов компания заплатила за определенный период времени.",
    )

    dividends = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Дивиденды",
        help_text="Это поле может показывать сумму денег, которую компания выплатила своим акционерам",
    )

    margin = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Маржа",
        help_text="Это поле показывает процентную прибыль компании, которая остается после вычета всех расходов от общей выручки.",
    )

    def __str__(self):
        return f'Финансовый показатели субъекта "{self.company.name}"'
