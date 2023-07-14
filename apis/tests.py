from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from enterprises.models import Company, OwnershipType, BusinessType
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token


class CompanyAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = get_user_model().objects.create_user(
            username="testuser", email="testuser@email.com", password="testpass123"
        )
        cls.no_owner = get_user_model().objects.create_user(
            username="testuser_2", email="testuser_2@email.com", password="testpass123"
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
        self.client.login()
        response_no_auth = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(
            response_no_auth.status_code, status.HTTP_403_FORBIDDEN
        )  # 403 no auth

        self.client.login(email="testuser@email.com", password="testpass123")
        response_with_auth = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(
            response_with_auth.status_code, status.HTTP_200_OK
        )  # 200 with auth
        self.assertEqual(Company.objects.count(), 1)
        self.assertContains(response_with_auth, self.company)

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
        self.assertEqual(
            response_detail.status_code, status.HTTP_200_OK
        )  # Object is present
        self.assertContains(response_detail, "Best Test Company")

        # Test created object
        created_company = Company.objects.get(slug="best-test-company")
        self.assertEqual(created_company.user, self.owner)

    def test_company_list_and_detail_api_permissions(self):
        """All authenticated users can create objects, but only the authors can delete and modify existing objects"""
        # no owner user
        self.client.login(email="testuser_2@email.com", password="testpass123")
        # patch request
        response_patch = self.client.patch(
            reverse(
                "api_v1:company_detail",
                kwargs={"slug": self.company.slug},
            ),
            data={"description": "Worst Test Company"},
            format="json",
        )
        # delete request
        response_delete = self.client.delete(
            reverse("api_v1:company_detail", kwargs={"slug": self.company.slug})
        )

        self.assertEqual(
            response_patch.status_code, status.HTTP_403_FORBIDDEN
        )  # 403 for patch
        self.assertEqual(
            response_delete.status_code, status.HTTP_403_FORBIDDEN
        )  # 403 for delete

        # owner user
        self.client.login(email="testuser@email.com", password="testpass123")

        response_patch = self.client.patch(
            reverse(
                "api_v1:company_detail",
                kwargs={"slug": self.company.slug},
            ),
            data={"description": "Worst Test Company"},
            format="json",
        )  # patch description field
        self.assertEqual(
            response_patch.status_code, status.HTTP_200_OK
        )  # 200 for patch
        self.assertEqual(
            Company.objects.get(slug=self.company.slug).description,
            "Worst Test Company",
        )  # description patched

        response_delete = self.client.delete(
            reverse("api_v1:company_detail", kwargs={"slug": self.company.slug})
        )  # delete company object
        self.assertEqual(
            response_delete.status_code, status.HTTP_204_NO_CONTENT
        )  # 204 object deleted
        with self.assertRaises(ObjectDoesNotExist):
            Company.objects.get(slug=self.company.slug)  # exception obj doesn't exist

    def test_token_auth(self):
        response_anon = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(
            response_anon.status_code, status.HTTP_403_FORBIDDEN
        )  # anon 403

        token = Token.objects.create(user=self.owner).key  # token for user
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token)  # login via token
        response_user = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(response_user.status_code, status.HTTP_200_OK)

        self.client.logout()
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + token
        )  # login via Bearer <token>
        response_user = self.client.get(reverse("api_v1:company_list"))
        self.assertEqual(response_user.status_code, status.HTTP_200_OK)

    def test_rest_registration(self):
        """Check CustomRegisterSerializer with new fields: first_name, last_name, phone_number, middle_name"""

        user_data = {
            "username": "testuser_3",
            "first_name": "Jack",
            "last_name": "Fry",
            "middle_name": "Ben",
            "email": "testuser_3@email.com",
            "phone_number": "77771023215",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        # api rest_register dj_rest_auth.registration
        response_register = self.client.post(
            reverse("rest_register"), data=user_data, format="json"
        )
        # Status - user created
        self.assertEqual(response_register.status_code, status.HTTP_204_NO_CONTENT)

        registered_user = get_user_model().objects.get(email="testuser_3@email.com")
        # check some fields
        self.assertEqual(registered_user.first_name, "Jack")
        self.assertEqual(registered_user.middle_name, "Ben")
        self.assertEqual(
            registered_user.phone_number.as_international, "+7 777 102 3215"
        )

    def test_user_model_view_set(self):
        self.client.login(email="testuser@email.com", password="testpass123")  # login
        response_user_list = self.client.get(reverse("api_v1:user-list"))  # user-list api
        self.assertEqual(response_user_list.status_code, status.HTTP_403_FORBIDDEN)  # only admin

        response_user_detail = self.client.get(
            reverse("api_v1:user-detail", kwargs={"pk": self.owner.pk})
        )  # user detail

        self.assertEqual(response_user_detail.status_code, status.HTTP_403_FORBIDDEN)  # only admin
        # self.assertContains(response_user_detail, text="testuser@email.com")  # email exists
