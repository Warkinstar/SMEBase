from django.test import TestCase
from .models import *


class OwnershipTypeTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.ownership_type = OwnershipType.objects.create(
            name="ИП", description="Индивидуальный предприниматель"
        )

    def test_ownership_type_content(self):
        self.assertEqual(self.ownership_type.name, "ИП")
        self.assertEqual(self.ownership_type.description, "Индивидуальный предприниматель")
