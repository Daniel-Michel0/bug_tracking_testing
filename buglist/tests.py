from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from database.models import Proyecto, ReporteBug, Bug

# Create your tests here.

class BuglistTestCase(TestCase):

    def setUp(self):
        # Crea 5 proyectos de muestra
        self.proyectos = []
        for i in range(1, 6):
            proyecto = Proyecto.objects.create(nombre_proyecto=f'Proyecto de prueba {i}')
            self.proyectos.append(proyecto)

        # Crea 25 reportes de bugs de muestra, asignando 5 reportes a cada proyecto
        reportes = []
        for i in range(1, 26):
            proyecto = self.proyectos[(i - 1) % 5]  # Asigna 5 reportes a cada proyecto en un ciclo
            reporte = ReporteBug.objects.create(
                titulo=f'Reporte de prueba {i}',
                fecha_reporte='2023-10-01',
                id_proyecto=proyecto
            )
            reportes.append(reporte)

        # Crea 5 bugs de muestra, asignando 1 bug a cada proyecto
        for i in range(1, 6):
            proyecto = self.proyectos[i - 1]
            bug = Bug.objects.create(
                titulo=f'Bug de prueba {i}',
                fecha_reporte='2023-10-01',
                estado='ASIGNADO',
                id_proyecto=proyecto
            )

    
