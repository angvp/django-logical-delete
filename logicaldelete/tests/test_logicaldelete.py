from django.db import models
from django.test import SimpleTestCase
from logicaldelete.models import Model


class ModelTest(Model):
    name = models.CharField(max_length=50)


class LogicalDeleteTestCase(SimpleTestCase):

    def test_init_fields(self):
        obj = ModelTest(name='test_name')

        self.assertIsNotNone(obj.date_created)
        self.assertIsNotNone(obj.date_modified)
        self.assertIsNone(obj.date_removed)