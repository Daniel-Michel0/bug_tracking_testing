import os
from typing import Any
from django.core.wsgi import get_wsgi_application
from database.models import *
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bug_tracking.settings")
application = get_wsgi_application()

class Command(BaseCommand):
    def handle(self, *args, **options):

        user = User.objects.create_user(
            username='testadmin',
            password='adminpass123',
            is_superuser=True,
            is_staff=True,
            email="test@admin.com"
        )
        
        user.save()

        usuario = Usuario.objects.create(
            user=user,
        )

        usuario.save()

        proyecto = Proyecto.objects.create(
            nombre_proyecto='Facebook',
        )

        proyecto.save()

        programador = Programador.objects.create(
            user= user,
        )

        programador.save()

        cargo = Cargo.objects.create(
            cargo = 'Programador',
            id_programador = programador,
            id_proyecto = proyecto,
        )

        cargo.save()

        bug = Bug.objects.create(
            titulo='Bug 1',
            descripcion='Descripcion 1',
            fecha_reporte=datetime.now(),
            id_programador=programador,
            id_proyecto=proyecto,
            estado='EN PROCESO',
            prioridad='ALTA',
        )

        bug.save()

        reporte = ReporteBug.objects.create(
            titulo='Reporte 1',
            reporte='Descripcion 1',
            fecha_reporte=datetime.now(),
            id_usuario=usuario,
            id_proyecto=proyecto,
            id_bug = bug,
            estado='APROBADO',
        )

        reporte.save()

        # Crear 20 bugs
        for i in range(20):
            bug = Bug.objects.create(
                titulo=f'Bug {i}',
                descripcion=f'Descripcion {i}',
                fecha_reporte=datetime.now(),
                id_programador=programador,
                id_proyecto=proyecto,
                estado='EN PROCESO',
                prioridad='ALTA',
            )

            bug.save()

        self.stdout.write(self.style.SUCCESS('La base de datos se ha llenado correctamente.'))