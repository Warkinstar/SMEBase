from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from enterprises.models import Company, OwnershipType, BusinessType
from django.contrib.auth import get_user_model


class APITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        owner = get_user_model().objects.create_user(
            username="testuser", password="testpass123"
        )
        ownership_type = OwnershipType.objects.create(name="ИП")
        business_type = BusinessType.objects.create(name="Рестораны")
        cls.company = Company.objects.create(
            name="Бисер",
            user=owner,
            tax_id="123456789123",
            ownership_type=ownership_type,
            business_type=business_type,
            description="Ресторан",
            address="8-10-55",
            phone_number="+77771028330",
            email="warkins@mail.ru",
        )

    def test_api_listview(self):
        response = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertContains(response, self.company)

    def test_api_detailview(self):
        response = self.client.get(reverse("api_v1:company_detail", kwargs={"slug": self.company.slug}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertContains(response, self.company)

