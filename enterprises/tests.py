from django.test import TestCase
from .models import *
from django.contrib.auth import get_user_model


class OwnershipTypeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        cls.ownership_type = OwnershipType.objects.create(
            name="ИП", description="Индивидуальный предприниматель"
        )
        cls.business_type = BusinessType.objects.create(
            name="Рестораны", description="Ресторанное дело"
        )
        cls.company = Company.objects.create(
            name="Бисер",
            user=cls.owner,
            tax_id="123456789123",
            ownership_type=cls.ownership_type,
            business_type=cls.business_type,
            description="Ресторан",
            address="8-10-55",
            phone_number="+77771028330",
            email="warkins@mail.ru",
        )

    def test_ownership_and_business_type_content(self):
        self.assertEqual(self.ownership_type.name, "ИП")
        self.assertEqual(
            self.ownership_type.description, "Индивидуальный предприниматель"
        )
        self.assertEqual(self.business_type.name, "Рестораны")
        self.assertEqual(self.business_type.description, "Ресторанное дело")

    def test_company_content(self):
        self.assertEqual(self.company.name, "Бисер")
        self.assertEqual(self.company.user.id, self.owner.id)
        self.assertEqual(self.company.tax_id, "123456789123")
        self.assertEqual(self.company.ownership_type, self.company.ownership_type)
        self.assertEqual(self.company.business_type, self.company.business_type)
        self.assertEqual(self.company.description, "Ресторан")
        self.assertEqual(self.company.address, "8-10-55")
        self.assertEqual(self.company.phone_number, "+77771028330")
        self.assertEqual(self.company.email, "warkins@mail.ru")
