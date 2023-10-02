from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from database.models import Proyecto, ReporteBug, Bug, Programador, Usuario
from django.contrib.auth import get_user_model

class BuglistTestCase(TestCase):

    def setUp(self):

        # Crea un usuario de muestra
        usuario = User.objects.create_user(
            username='usuario',
            password='usuario123',
            email='usuario@usuario',
        )

        usuario_ = Usuario.objects.last()

        # Crea 5 usuarios programadores de muestra
        programadores = []
        for i in range(1, 6):
            programador = Programador.objects.create(
                user=User.objects.create_user(
                    username=f'programador{i}',
                    password=f'programador{i}123',
                    email=f'programador{i}@email',
                )
            )
            programadores.append(programador)

        # Crea 5 proyectos de muestra
        proyectos = []
        for i in range(1, 6):
            proyecto = Proyecto.objects.create(nombre_proyecto=f'Proyecto de prueba {i}')
            proyectos.append(proyecto)

        # Crea 25 reportes de bugs de muestra, asignando 5 reportes a cada proyecto
        for i in range(1, 26):
            proyecto = proyectos[(i - 1) % 5]  # Asigna 5 reportes a cada proyecto en un ciclo
            ReporteBug.objects.create(
                titulo=f'Reporte de prueba {i}',
                fecha_reporte='2023-10-01',
                id_proyecto=proyecto,
                id_usuario= usuario_,
            )

        # Crea 5 bugs de muestra, asignando 1 bug a cada proyecto
        for i in range(1, 6):
            proyecto = proyectos[i - 1]
            programador = programadores[i - 1]
            Bug.objects.create(
                titulo=f'Bug de prueba {i}',
                fecha_reporte='2023-10-01',
                estado='ASIGNADO',
                id_proyecto=proyecto,
                id_programador=programador,
            )