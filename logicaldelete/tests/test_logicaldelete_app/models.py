from django.db import models
from logicaldelete.models import Model


class ModelTest(Model):
    name = models.CharField(max_length=50)



