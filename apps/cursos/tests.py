from django.test import TestCase
from django.test import TestCase
from pymysql import NULL
# Create your tests here.
from .serializers import *

class CursoTest(TestCase):

   def setUp(self) :
      self.curso = Curso(nombre = 'Carlos')
      self.cursoserial = CursoSerializer(data=self.curso)

   def test_self_curso(self):
      self.assertIs(self.curso.nombre, 'Carlos')
   
   def test_curso_serial(self):
      
      self.assertIs(self.cursoserial.is_valid(),True)
      print(self.cursoserial.errors)
