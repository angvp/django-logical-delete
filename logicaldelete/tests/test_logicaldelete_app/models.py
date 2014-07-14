from django.db import models
from logicaldelete.models import Model


class ModelTest(Model):
    name = models.CharField(max_length=50)


class ModelTestFKLogical(Model):
    """
    ForeignKey class to ModelTest that inherits from
    logical detele
    """
    child_name = models.CharField(max_length=50)
    father = models.ForeignKey(ModelTest)


class ModelTestFKNotLogical(models.Model):
    """
    ForeignKey class to ModelTest that inherits from
    logical detele
    """
    child_name = models.CharField(max_length=50)
    father = models.ForeignKey(ModelTest)


class ModelTestManagersNotLogical(models.Model):
    """
    ForeignKey class to ModelTestFKNotLogical
    that does not inherits from logical detele
    """
    double_child_name = models.CharField(max_length=50)
    father = models.ForeignKey(ModelTestFKNotLogical)