from django.db import models
from enterprises.models import Company


class BaseModel(models.Model):
    """Базовая абстрактная модель"""

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ProductCategory(BaseModel):
    """Категория продукта"""

    name = models.CharField(
        "Категория продукта",
        max_length=255,
        help_text="Электроника, одежда, услуги и т.д.",
    )
    description = models.TextField("Описание категории продукта", blank=True)

    class Meta:
        verbose_name_plural = "Product Categories"


class ProductType(BaseModel):
    """Тип продукта"""

    product_category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        related_name="types",
        help_text="Категория продукта",
    )
    name = models.CharField(
        "Тип продукта", max_length=255, help_text="Фрукты, овощи, брюки и т. д."
    )
    description = models.TextField("Описание типа продукта", blank=True)


class Product(BaseModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="products"
    )
    type = models.ForeignKey(
        ProductType,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="Тип продукта",
    )
    name = models.CharField("Название продукта", max_length=255)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    description = models.TextField("Описание продукта", blank=True)
    image = models.ImageField("Изображение продукта", upload_to="product_images", blank=True)
