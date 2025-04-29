import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from zimit_manager import models
from zimit_manager.enums import ExecutionStatus, ScopeType, Urgency

factory_faker = Faker()

# pylint:disable=too-few-public-methods


class ZimitExecutionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ZimitExecution
        # sqlalchemy_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n)
    memory = factory_faker.random_element(["4g", "500m", "8g", "1g"])
    result_link = None
    output_dir = "output"
    status = ExecutionStatus(factory_faker.random_int(-1, 2))
    workers = factory_faker.random_int(1, 8)


class ZimitTaskFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ZimitTask
        # sqlalchemy_get_or_create = ('id',)

    id = factory.Sequence(lambda n: n)
    description = factory_faker.text(max_nb_chars=30)
    extra_hops = factory_faker.random_int(0, 3)
    name = factory_faker.catch_phrase()
    requested_by = factory_faker.first_name_female()
    scope_type = ScopeType(factory_faker.random_int(0, 1))
    short_name = name.lower()[:5]
    urgency = Urgency(factory_faker.random_int(0, 3))
    url = factory_faker.url()
