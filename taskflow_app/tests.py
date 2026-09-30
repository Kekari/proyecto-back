from django.test import TestCase, Client
from django.urls import reverse
from taskflow_app.models import (
    Usuario,
    EspacioTrabajo,
    RolColaborador,
    VisibilidadTablero,
    Tablero,
    Lista,
    Prioridad,
    Tarjeta,
)


class TaskFlowModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre="Kekari Test",
            correo="kekari@test.com",
            rut="12.345.678-9",
            cargo="Developer"
        )
        self.rol = RolColaborador.objects.create(
            codigo="ADMIN",
            nombre="Administrador"
        )
        self.visibilidad = VisibilidadTablero.objects.create(
            codigo="PUBLICO",
            nombre="Público"
        )
        self.espacio = EspacioTrabajo.objects.create(
            nombre="Espacio Test",
            creador=self.usuario
        )
        self.tablero = Tablero.objects.create(
            nombre="Tablero Test",
            espacio=self.espacio,
            creador=self.usuario,
            visibilidad=self.visibilidad
        )
        self.lista = Lista.objects.create(
            tablero=self.tablero,
            nombre="Por Hacer",
            posicion=1
        )
        self.prioridad = Prioridad.objects.create(
            codigo="ALTA",
            nombre="Alta",
            color="#ef4444",
            nivel=3
        )
        self.tarjeta = Tarjeta.objects.create(
            lista=self.lista,
            titulo="Tarjeta de prueba",
            creador=self.usuario,
            prioridad=self.prioridad
        )

    def test_creacion_usuario(self):
        self.assertEqual(str(self.usuario), "Kekari Test (kekari@test.com)")
        self.assertTrue(self.usuario.habilitado)

    def test_creacion_tablero(self):
        self.assertEqual(str(self.tablero), "Tablero Test")
        self.assertEqual(self.tablero.espacio.nombre, "Espacio Test")

    def test_creacion_lista_y_tarjeta(self):
        self.assertEqual(self.lista.tarjetas.count(), 1)
        self.assertEqual(self.tarjeta.titulo, "Tarjeta de prueba")
        self.assertFalse(self.tarjeta.completada)


class TaskFlowViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nombre="Kekari Test",
            correo="kekari.view@test.com"
        )
        self.vis = VisibilidadTablero.objects.create(
            codigo="ESPACIO",
            nombre="Espacio"
        )
        self.espacio = EspacioTrabajo.objects.create(
            nombre="Espacio View Test",
            creador=self.usuario
        )
        self.tablero = Tablero.objects.create(
            nombre="Tablero View Test",
            espacio=self.espacio,
            creador=self.usuario,
            visibilidad=self.vis
        )
        self.lista1 = Lista.objects.create(
            tablero=self.tablero,
            nombre="Columna 1",
            posicion=1
        )
        self.lista2 = Lista.objects.create(
            tablero=self.tablero,
            nombre="Columna 2",
            posicion=2
        )
        self.tarjeta = Tarjeta.objects.create(
            lista=self.lista1,
            titulo="Mover esta tarjeta",
            creador=self.usuario
        )

    def test_vista_inicio(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TaskFlow")

    def test_vista_tableros(self):
        response = self.client.get(reverse('tableros'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tablero View Test")

    def test_vista_detalle_tablero(self):
        response = self.client.get(reverse('detalle_tablero', args=[self.tablero.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Columna 1")
        self.assertContains(response, "Mover esta tarjeta")

    def test_mover_tarjeta(self):
        response = self.client.post(
            reverse('mover_tarjeta', args=[self.tarjeta.id]),
            {'nueva_lista_id': self.lista2.id}
        )
        self.assertEqual(response.status_code, 302)
        self.tarjeta.refresh_from_db()
        self.assertEqual(self.tarjeta.lista.id, self.lista2.id)

    def test_crear_tarjeta_rapida(self):
        response = self.client.post(
            reverse('crear_tarjeta', args=[self.lista1.id]),
            {'titulo': 'Nueva tarjeta test'}
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tarjeta.objects.filter(titulo='Nueva tarjeta test').exists())
