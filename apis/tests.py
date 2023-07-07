from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from enterprises.models import Company, OwnershipType, BusinessType
from django.contrib.auth import get_user_model


class CompanyAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        cls.ownership_type = OwnershipType.objects.create(name="ИП")
        cls.business_type = BusinessType.objects.create(name="Рестораны")
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

    def test_api_listview(self):
        response = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertContains(response, self.company)

    def test_api_detailview(self):
        self.client.login(email="testuser@email.com", password="testpass123")
        response = self.client.get(
            reverse("api_v1:company_detail", kwargs={"slug": self.company.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Company.objects.count(), 1)
        self.assertContains(response, self.company)

    def test_api_create_company_listview(self):
        """Create can only auth users"""
        self.client.login(email="testuser@email.com", password="testpass123")  # login
        company_data = {
            "name": "Best Test Company",
            "slug": "best-test-company",
            "tax_id": "121121111116",
            "description": "Description for best company",
            "address": "8-10-55",
            "phone_number": "+77773038230",
            "email": "warkinstar@gmail.com",
            # "website": "",
            "ownership_type": self.ownership_type.pk,
            "business_type": self.business_type.pk,
        }  # some data
        response_post = self.client.post(
            reverse("api_v1:company_list"), data=company_data, format="json"
        )  # post request to create object
        self.assertEqual(
            response_post.status_code, status.HTTP_201_CREATED
        )  # Check created object

        # Check detail page for created object
        response_detail = self.client.get(
            reverse("api_v1:company_detail", kwargs={"slug": company_data["slug"]})
        )
        self.assertEqual(response_detail.status_code, status.HTTP_200_OK)  # Object is present
        self.assertContains(response_detail, "Best Test Company")

        # Test created object
        created_company = Company.objects.get(slug="best-test-company")
        self.assertEqual(created_company.user, self.owner)
