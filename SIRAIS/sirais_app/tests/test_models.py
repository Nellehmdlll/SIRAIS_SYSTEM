from django.test import TestCase
from models import Project

class ProjectTestCase(TestCase):
    def test_create_model(self):
        my_instance = Project.objects.create(name="Test")
        self.assertEqual(my_instance.name, "Test")
