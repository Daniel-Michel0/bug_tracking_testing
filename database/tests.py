from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *
from database.admin import ReasignacionBugAdmin
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite

# Create your tests here.

class DataBaseTest(TestCase):
    def setUp(self):
        #crear usuarios                             

        u1 = Usuario.objects.create("grupo7@is2.com")
        u1.save()

        #crear programadores

        p1 = Programador.objects.create(correo_programador="jvidal@udec.cl", nombre_programador="Javier Vidal")
        p2 = Programador.objects.create(correo_programador="jlopez@udec.cl", nombre_programador="Jorge Lopez")

        p1.save()
        p2.save()
        #crear proyectos

        proyecto1 = Proyecto.objects.create(nombre_proyecto="Infoda",)

        proyecto1.save()

        #crear cargos

        c1 = Cargo(
            programador = p1,
            proyecto = proyecto1,
        )

        c2 = Cargo(
            programador = p2,
            proyecto = proyecto1,
        )

        c1.save()
        c2.save()

        #crear reporteBug

        r1 = ReporteBug.objects.create(
            titulo= "no puedo entrar",
            reporte= "Usando Brave no puedo entrar al sistema",
            correo_usuario= u1,
        )

        r1.save()


        #crear Bug

        b1 = Bug.objects.create(
            descripcion = "no se puede entrar desde Brave",
            prioridad   = "media",
            estado      = "nuevo", 
            proyecto    = proyecto1,
            programador = p1,
        )

        b1.save()

        r1.bug = b1

        r1.save()
        
    def usuarioTest(self):
        u1 = Usuario.objects.get(correo_usuario="grupo7@is2.com")
        

class ReasignacionBugAdminTestCase(TestCase):
    def setUp(self):
        # Configura el sitio de administración
        self.site = AdminSite()
        self.reasignacion_admin = ReasignacionBugAdmin(Reasignacion, self.site)

        # Crea usuarios y otros objetos necesarios
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.programador1 = Programador.objects.create(user=self.user1)
        self.programador2 = Programador.objects.create(user=self.user2)
        self.proyecto = Proyecto.objects.create(nombre_proyecto='Proyecto de prueba')
        self.bug = Bug.objects.create(
            titulo='Bug de prueba',
            descripcion='Descripción del bug de prueba',
            prioridad='BAJA',
            estado='PENDIENTE',
            id_proyecto=self.proyecto,
            id_programador=self.programador1
        )
        
    # Prueba para  realizar una reasignación a un mismo empleado
    def test_reasignacion_same_person(self):
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador1,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        # Se verifica que se genere la excepción de validación y se intenta guardar la reasignación
        with self.assertRaises(ValidationError) as context:
            reasignacion.full_clean()
        # Se verifica que la excepción de validación sea el mensaje establecido
        self.assertIn("No se puede reasignar a la misma persona.", str(context.exception))
    
    # Prueba para realizar una reasignación válida a un empleado diferente
    def test_reasignacion_different_person(self):
        
        user = User.objects.create(username='usuario_prueba')
        programador2 = Programador.objects.create(user=user)


        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        # Se guarda la reasignación
        reasignacion.full_clean()
    
    
    # Prueba para verificar actualización de bug al nuevo empleado
    def test_reasignacion_updates_bug_programador(self):
        # Realiza una reasignación válida
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        # Se guarda la reasignación y se verifica que se actualice el bug
        response = self.reasignacion_admin.save_model(request=None, obj=reasignacion, form=None, change=None)
        bug = Bug.objects.get(id_bug=self.bug.id_bug)

        # Se verifica que el bug ahora tenga el nuevo empleado asignado
        self.assertEqual(bug.id_programador, self.programador2)
    
    # Prueba para verificar actualización de solicitud de reasignación al ser aprobada
    def test_reasignacion_updates_estado(self):
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )

        # Se guarda la reasignación y se verifica que el estado se actualice a 'APROBADO'
        response = self.reasignacion_admin.save_model(request=None, obj=reasignacion, form=None, change=None)
        reasignacion_actualizada = Reasignacion.objects.get(id_reasignacion=reasignacion.id_reasignacion)

        # Se verifica que el estado de la reasignación ahora sea 'APROBADO'
        self.assertEqual(reasignacion_actualizada.estado, "('APROBADO', 'reasignación aprobada')")

    
        