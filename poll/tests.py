import unittest
# from django.test import TestCase
from poll.models import Question
from django.utils import timezone
from django.urls import reverse, resolve
# Create your tests here.
class QuestionTest(unittest.TestCase):

    def create_question(self, title="only for test",status="ems"):
        return Question(title=title,status=status)

    def test_question_creation(self):
        e = self.create_question()
        self.assertTrue(isinstance(e,Question))
        self.assertEqual(e.__str__(),e.title)
# Create your tests here.