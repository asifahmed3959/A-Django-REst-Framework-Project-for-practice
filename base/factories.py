import factory

from .models import *

from faker import Factory

faker = Factory.create()

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = faker.email()
    first_name = faker.name()
    last_name = faker.name()
    password = 'pingpong1234'


class QuoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Quote

    author = factory.SubFactory(UserFactory)
    quote = faker.text()



class PublicationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Publication

    quote = factory.SubFactory(QuoteFactory)
    name = faker.name()
