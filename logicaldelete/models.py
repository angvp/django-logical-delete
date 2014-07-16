from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from logicaldelete import managers

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


class Model(models.Model):
    """
    This base model provides date fields and functionality to enable logical
    delete functionality in derived models.
    """

    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    date_removed = models.DateTimeField(null=True, blank=True)

    objects = managers.LogicalDeletedManager()

    def active(self):
        return self.date_removed is None
    active.boolean = True

    def delete(self):
        '''
        Soft delete all fk related objects that
        inherit from logicaldelete class
        '''

        # Fetch related models
        related_objs = [relation.get_accessor_name() for
                        relation in self._meta.get_all_related_objects()]

        # Iterate & Delete them
        for objs_model in related_objs:
            # Retrieve all related objects
            try:
                objs_query = getattr(self, objs_model)
                objs = objs_query.all()

                for obj in objs:
                    # Checking if inherits from logicaldelete
                    if issubclass(obj.__class__, Model):
                        obj.delete()
            except:
                # The attribute  or relation  may not
                # be instanciated.
                pass

        # Soft delete the object
        self.date_removed = timezone.now()
        self.save()

    def undelete(self):
        '''
        UnSoft delete all fk related objects that
        inherit from logicaldelete class
        '''

        # Fetch related models
        related_objs = [relation.get_accessor_name() for
                        relation in self._meta.get_all_related_objects()]

        # Iterate & Delete them
        for objs_model in related_objs:
            # Retrieve all related objects
            try:
                objs_query = getattr(self, objs_model)
                objs = objs_query.all_with_deleted()

                for obj in objs:
                    # Checking if inherits from logicaldelete
                    if issubclass(obj.__class__, Model):
                        obj.undelete()
            except:
                # The attribute  or relation  may not
                # be instanciated or doesnt have the Attributes
                pass

        self.date_removed = None
        self.save()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date_modified = timezone.now()

        if self.date_removed:
            # Patch for reupdating the DeletedTime
            self.date_removed = timezone.now()

        super(Model, self).save(force_insert, force_update, using,
                                update_fields)

    class Meta:
        abstract = True
