from django.test import TestCase

from logicaldelete.tests.test_logicaldelete_app. \
    models import (ModelTest, ModelTestFKLogical,
                   ModelTestFKNotLogical, ModelTestManagersNotLogical)


class LogicalDeleteTestCase(TestCase):
    def setUp(self):
        self.obj_father = ModelTest.objects.create(
            name='test_name')
        self.obj_child_fk = ModelTestFKLogical.objects.create(
            child_name='fk_name', father=self.obj_father)
        self.obj_child_nofk = ModelTestFKNotLogical.objects.create(
            child_name='nofk_name', father=self.obj_father)

        # Un related objects that shouldn't be touch
        self.obj_father_2 = ModelTest.objects.create(
            name='test_name_2')
        self.obj_child_fk_2 = ModelTestFKLogical.objects.create(
            child_name='fk_name_2', father=self.obj_father_2)
        self.obj_child_nofk_2 = ModelTestFKNotLogical.objects.create(
            child_name='nofk_name_2', father=self.obj_father_2)

        # Objects for manager tests
        self.double_child = ModelTestManagersNotLogical.objects.create(
            double_child_name='double_name', father=self.obj_child_nofk_2)
        self.double_child_2 = ModelTestManagersNotLogical.objects.create(
            double_child_name='double_name_2', father=self.obj_child_nofk_2)

    def test_init_fields(self):
        """
        First test, testing save()
        """
        self.assertIsNotNone(self.obj_father.date_created)
        self.assertIsNotNone(self.obj_father.date_modified)
        self.assertIsNone(self.obj_father.date_removed)

    def test_init_fields_status(self):
        self.assertTrue(self.obj_father.active())
        self.obj_father.delete()
        self.obj_father.save()
        self.assertFalse(self.obj_father.active())
        self.obj_father.undelete()
        self.assertTrue(self.obj_father.active())

    def test_delete_undelete(self):
        """
        Test cascade deleting with an object
        that has a son inheriting from logical delete
        and another son that inherits from django.models
        """

        # Check all objects in place
        self.assertEqual(ModelTest.objects.count(), 2)
        self.assertEqual(ModelTestFKNotLogical.objects.count(), 2)
        self.assertEqual(ModelTestFKLogical.objects.count(), 2)

        # Cascade deleting
        self.obj_father.delete()

        self.assertEqual(ModelTest.objects.count(), 1)
        self.assertEqual(ModelTestFKNotLogical.objects.count(), 2)
        self.assertEqual(ModelTestFKLogical.objects.count(), 1)

        self.assertIsNotNone(self.obj_father.date_removed)
        self.assertIsNone(self.obj_father_2.date_removed)

        self.obj_child_fk = ModelTestFKLogical.objects.get(id=1)
        self.obj_child_fk_2 = ModelTestFKLogical.objects.get(id=2)
        self.assertIsNotNone(self.obj_child_fk.date_removed)
        self.assertIsNone(self.obj_child_fk_2.date_removed)

        # Cascade undeleting
        self.obj_father.undelete()

        self.assertEqual(ModelTest.objects.count(), 2)
        self.assertEqual(ModelTestFKNotLogical.objects.count(), 2)
        self.assertEqual(ModelTestFKLogical.objects.count(), 2)

        self.assertIsNone(self.obj_father.date_removed)
        self.assertIsNone(self.obj_father_2.date_removed)

        self.obj_child_fk = ModelTestFKLogical.objects.get(id=1)
        self.obj_child_fk_2 = ModelTestFKLogical.objects.get(id=2)
        self.assertIsNone(self.obj_child_fk.date_removed)
        self.assertIsNone(self.obj_child_fk_2.date_removed)

    def test_managers(self):
        self.obj_father.delete()

        # Test filter filter
        self.assertIsNotNone(ModelTest.objects.filter(pk=1))
        self.assertEqual(ModelTest.objects.filter(
            name='test_name').count(), 0)

        # Test all_with_deleted, only_deleted
        self.assertEqual(ModelTest.objects.only_deleted().count(), 1)
        self.assertEqual(ModelTest.objects.all_with_deleted().count(), 2)
        self.assertEqual(ModelTest.objects.all().count(), 1)

        # Test get
        self.assertIsNotNone(ModelTest.objects.get(id=1))
        self.assertIsNotNone(ModelTest.objects.get(id=2))

    def test_related_managers(self):
        self.obj_father.delete()

        self.obj_child_nofk_2.modeltestmanagersnotlogical_set.all()
        self.obj_father.modeltestfklogical_set.all_with_deleted()
        self.assertEqual(self.obj_father.modeltestfklogical_set.all().count(),
                         0)
        self.assertEqual(self.obj_father.modeltestfklogical_set.all_with_deleted().count(),
                         1)
        self.assertEqual(self.obj_father.modeltestfknotlogical_set.all().count(),
                         1)
