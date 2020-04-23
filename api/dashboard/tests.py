from django.test import TestCase
from rest_framework.test import APITestCase

from django.urls import reverse

from base.models import *
from base.factories import *

from faker import Faker

fake = Faker()

class QuoteApiTestCase(APITestCase):
    def setUp(self):
        super(QuoteApiTestCase, self).setUp()
        self.user = UserFactory.create(first_name = fake.name(), last_name = fake.name(), email = fake.email()
                                  , username = fake.name(), password = fake.password)
        self.url = reverse('dashboard:quote-list')
        self.client.force_authenticate(user=self.user)

    def test_can_create_quote(self):
        user1 = UserFactory.create(first_name = fake.name(), last_name = fake.name(), email = fake.email()
                                  , username = fake.name(), password = fake.password)
        user2 = UserFactory.create(first_name = fake.name(), last_name = fake.name(), email = fake.email()
                                  , username = fake.name(), password = fake.password)
        user3 = UserFactory.create(first_name = fake.name(), last_name = fake.name(), email = fake.email()
                                  , username = fake.name(), password = fake.password)
        data = {
            "quote": 'Hello World',
            'author_id': self.user.id,
        }

        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code,200)