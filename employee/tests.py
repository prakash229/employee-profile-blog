import unittest
from django.test import TestCase
from employee.models import Profile
from django.utils import timezone
#from django.urlresolvers import reverse
# Create your tests here.
class ProfileTest(TestCase):

    def create_employee(self,user="chandraprakash", designation="constlt"):
        return Profile(user=user,designation=designation)
        
    # def test_employee_creation(self):
    #     e = self.create_employee()
    #     self.assertTrue(e.Profile)
    #     self.assertEqual(e.__str__(),e.user)
from django.urls import reverse