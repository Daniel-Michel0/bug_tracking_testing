from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from database.models import Proyecto, ReporteBug, Bug, Programador, Usuario
from django.contrib.auth import get_user_model

class BuglistTestCase(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "test@email.com"

        self.user = get_user_model().objects.create_user(
            self.username,
            self.email,
            self.password
        )

        self.programador = Programador.objects.create(
            user=self.user,
        )

        self.usuario = Usuario.objects.create(
            user=self.user,
        )

        self.proyecto = Proyecto.objects.create(
            nombre_proyecto="Proyecto de prueba"
        )

        self.reporte = ReporteBug.objects.create(
            id_proyecto=self.proyecto,
            titulo="Reporte de prueba",
            reporte="Este es un reporte de prueba",
            fecha_reporte="2020-01-01",
            estado="Pendiente",
            id_usuario = self.usuario
        )

        self.bug = Bug.objects.create(
            id_reporte=self.reporte,
            titulo="Bug de prueba",
            descripcion="Este es un bug de prueba",
            fecha_reporte="2020-01-01",
            estado="Pendiente",
            id_programador=self.programador
        )

