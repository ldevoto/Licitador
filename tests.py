import clases as c
import unittest

#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestLote(unittest.TestCase):
    def setUp(self):
        self.id = 1
        self.descripcion = "Lote 1"
        self.facturacion_media_anual = 1000.00
        self.recursos_financieros = 1500.00
        self.experiencia = 2000.00
        self.lote = c.Lote(self.id, self.facturacion_media_anual, self.recursos_financieros, self.experiencia)
        self.lote.descripcion = self.descripcion

    def test_atributos(self):
        self.assertEqual(self.lote.id, self.id)
        self.assertEqual(self.lote.facturacion_media_anual, self.facturacion_media_anual)
        self.assertEqual(self.lote.recursos_financieros, self.recursos_financieros)
        self.assertEqual(self.lote.experiencia, self.experiencia)
        self.assertEqual(self.lote.descripcion, self.descripcion)


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestContrato(unittest.TestCase):
    def setUp(self):
        self.anio = 2017
        self.valor = 1000.00
        self.contrato = c.Contrato(self.anio, self.valor)

    def test_atributos(self):
        self.assertEqual(self.contrato.anio, self.anio)
        self.assertEqual(self.contrato.valor, self.valor)


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestEmpresa(unittest.TestCase):
    def setUp(self):
        self.id = 1
        self.nombre = "Empresa 1"
        self.facturacion_media_anual = 1000.00
        self.recursos_financieros = 1500.00
        self.contrato_1 = c.Contrato(2017, 1500.00)
        self.contrato_2 = c.Contrato(2017, 2000.00)
        self.empresa = c.Empresa(self.id, self.nombre, self.facturacion_media_anual, self.recursos_financieros, [self.contrato_1, self.contrato_2])

        self.facturacion_media_anual_empresa1 = 22000.00
        self.recursos_financieros_empresa1 = 22000.00
        self.facturacion_media_anual_empresa2 = 15000.00
        self.recursos_financieros_empresa2 = 15000.00
        self.valor_contrato1 = 2000.00
        self.valor_contrato2 = 5000.00
        self.valor_contrato3 = 6000.00
        self.valor_contrato4 = 12000.00
        self.contrato1 = c.Contrato(2017, self.valor_contrato1)
        self.contrato2 = c.Contrato(2017, self.valor_contrato2)
        self.contrato3 = c.Contrato(2017, self.valor_contrato3)
        self.contrato4 = c.Contrato(2017, self.valor_contrato4)
        self.contratos1 = [self.contrato1, self.contrato2, self.contrato3, self.contrato4]
        self.contratos2 = [self.contrato1, self.contrato2, self.contrato3]
        self.empresa1 = c.Empresa(1, "Empresa 1", self.facturacion_media_anual_empresa1, self.recursos_financieros_empresa1, self.contratos1)
        self.empresa2 = c.Empresa(2, "Empresa 2", self.facturacion_media_anual_empresa2, self.recursos_financieros_empresa2, self.contratos2)
        self.facturacion_media_anual_lote1 = 1000.00
        self.recursos_financieros_lote1 = 1000.00
        self.experiencia_lote1 = 1000.00
        self.facturacion_media_anual_lote2 = 5000.00
        self.recursos_financieros_lote2 = 5000.00
        self.experiencia_lote2 = 5000.00
        self.facturacion_media_anual_lote3 = 15000.00
        self.recursos_financieros_lote3 = 15000.00
        self.experiencia_lote3 = 15000.00
        self.facturacion_media_anual_lote4 = 150000.00
        self.recursos_financieros_lote4 = 150000.00
        self.experiencia_lote4 = 150000.00
        self.lote1 = c.Lote(1, self.facturacion_media_anual_lote1, self.recursos_financieros_lote1, self.experiencia_lote1)
        self.lote2 = c.Lote(2, self.facturacion_media_anual_lote2, self.recursos_financieros_lote2, self.experiencia_lote2)
        self.lote3 = c.Lote(3, self.facturacion_media_anual_lote3, self.recursos_financieros_lote3, self.experiencia_lote3)
        self.lote4 = c.Lote(4, self.facturacion_media_anual_lote4, self.recursos_financieros_lote4, self.experiencia_lote4)
        self.valor_oferta1_empresa1 = 5000.00
        self.valor_oferta2_empresa1 = 10000.00
        self.valor_oferta3_empresa1 = 50000.00
        self.valor_oferta4_empresa1 = 150000.00
        self.valor_oferta1_empresa2 = 5000.00
        self.valor_oferta2_empresa2 = 10000.00
        self.valor_oferta3_empresa2 = 50000.00
        self.oferta1_empresa1 = c.Oferta(self.empresa1, self.lote1, self.valor_oferta1_empresa1)
        self.oferta2_empresa1 = c.Oferta(self.empresa1, self.lote2, self.valor_oferta2_empresa1)
        self.oferta3_empresa1 = c.Oferta(self.empresa1, self.lote3, self.valor_oferta3_empresa1)
        self.oferta4_empresa1 = c.Oferta(self.empresa1, self.lote4, self.valor_oferta4_empresa1)
        self.oferta1_empresa2 = c.Oferta(self.empresa2, self.lote1, self.valor_oferta1_empresa2)
        self.oferta2_empresa2 = c.Oferta(self.empresa2, self.lote2, self.valor_oferta2_empresa2)
        self.oferta3_empresa2 = c.Oferta(self.empresa2, self.lote3, self.valor_oferta3_empresa2)
        self.conjunto_ofertas1 = c.ConjuntoOfertas()
        self.conjunto_ofertas2 = c.ConjuntoOfertas()
        self.conjunto_ofertas1.agregar_oferta(self.oferta1_empresa1)
        self.conjunto_ofertas1.agregar_oferta(self.oferta2_empresa1)
        self.conjunto_ofertas1.agregar_oferta(self.oferta3_empresa1)
        self.conjunto_ofertas2.agregar_oferta(self.oferta1_empresa2)
        self.conjunto_ofertas2.agregar_oferta(self.oferta2_empresa2)
        self.conjunto_ofertas2.agregar_oferta(self.oferta3_empresa2)
        self.adicional = c.Adicional(self.empresa, c.ConjuntoOfertas(), 100.00)
        self.posibilidad = c.Posibilidad(self.empresa1, self.adicional)

    def test_atributos(self):
        self.assertEqual(self.empresa.id, self.id)
        self.assertEqual(self.empresa.nombre, self.nombre)
        self.assertEqual(self.empresa.facturacion_media_anual(), self.facturacion_media_anual)
        self.assertEqual(self.empresa.recursos_financieros(), self.recursos_financieros)
        self.assertCountEqual(self.empresa.contratos(), [self.contrato_1, self.contrato_2])
        self.assertIsInstance(self.empresa.conjunto_ofertas, c.ConjuntoOfertas)
        self.assertEqual(self.empresa.conjunto_ofertas.valor(), 0.00)
        self.assertEqual(self.empresa.conjunto_ofertas.cantidad_ofertas(), 0)
        self.assertEqual(len(self.empresa.adicionales), 1)
        self.assertIsInstance(self.empresa.adicionales[0], c.AdicionalNulo)
        self.assertListEqual(self.empresa.posibilidades, [])

    def test_agregar_adicional(self):
        self.empresa.agregar_adicional(self.adicional)
        self.assertEqual(len(self.empresa.adicionales), 2)

    def test_asignar_conjunto_ofertas(self):
        self.empresa.asignar_conjunto_ofertas(self.conjunto_ofertas1)
        self.assertEqual(self.empresa.conjunto_ofertas, self.conjunto_ofertas1)

    def test_calcular_posibilidades(self):
        self.empresa1.asignar_conjunto_ofertas(self.conjunto_ofertas1)
        self.empresa2.asignar_conjunto_ofertas(self.conjunto_ofertas2)
        self.empresa1.calcular_posibilidades()
        self.assertEqual(len(self.empresa1.posibilidades), 7)
        self.assertTrue(any(posibilidad.valor() == self.oferta1_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta2_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta3_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta1_empresa1.valor + self.oferta2_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta1_empresa1.valor + self.oferta3_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta2_empresa1.valor + self.oferta3_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta1_empresa1.valor + self.oferta2_empresa1.valor + self.oferta3_empresa1.valor for posibilidad in self.empresa1.posibilidades))
        self.empresa2.calcular_posibilidades()
        self.assertEqual(len(self.empresa2.posibilidades), 3)
        self.assertTrue(any(posibilidad.valor() == self.oferta1_empresa2.valor for posibilidad in self.empresa2.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta2_empresa2.valor for posibilidad in self.empresa2.posibilidades))
        self.assertTrue(any(posibilidad.valor() == self.oferta1_empresa2.valor + self.oferta2_empresa2.valor for posibilidad in self.empresa2.posibilidades))
    
    def test_lotes_ofertados(self):
        self.empresa1.asignar_conjunto_ofertas(self.conjunto_ofertas1)
        self.assertCountEqual(self.empresa1.lotes_ofertados(), [self.lote1, self.lote2, self.lote3])
    
    def test_cantidad_lotes_ofertados(self):
        self.empresa1.asignar_conjunto_ofertas(self.conjunto_ofertas1)
        self.assertEqual(self.empresa1.cantidad_lotes_ofertados(), len([self.lote1, self.lote2, self.lote3]))

    def test_facturacion_media_anual(self):
        self.assertEqual(self.empresa1.facturacion_media_anual(), self.facturacion_media_anual_empresa1)

    def test_recursos_financieros(self):
        self.assertEqual(self.empresa1.recursos_financieros(), self.recursos_financieros_empresa1)
    
    def test_contratos(self):
        self.assertCountEqual(self.empresa1.contratos(), self.contratos1)
    
    def test_experiencia(self):
        self.posibilidad.agregar_oferta(self.oferta1_empresa1)
        self.assertEqual(self.empresa1.experiencia(self.posibilidad), 18000.00)
        self.posibilidad.agregar_oferta(self.oferta2_empresa1)
        self.posibilidad.agregar_oferta(self.oferta3_empresa1)
        self.assertEqual(self.empresa1.experiencia(self.posibilidad), 25000.00)
        self.posibilidad.conjunto_ofertas.agregar_oferta(self.oferta4_empresa1)
        self.assertEqual(self.empresa1.experiencia(self.posibilidad), 25000.00)

    def test_cumple_facturacion_media_anual(self):
        self.assertTrue(self.empresa1.cumple_facturacion_media_anual(self.facturacion_media_anual_empresa1 - 1000))
        self.assertFalse(self.empresa1.cumple_facturacion_media_anual(self.facturacion_media_anual_empresa1 + 1000))
    
    def test_cumple_recursos_financieros(self):
        self.assertTrue(self.empresa1.cumple_recursos_financieros(self.recursos_financieros_empresa1 - 1000))
        self.assertFalse(self.empresa1.cumple_recursos_financieros(self.recursos_financieros_empresa1 + 1000))

    def test_cumple_experiencia(self):
        self.posibilidad.agregar_oferta(self.oferta1_empresa1)
        self.assertTrue(self.empresa1.cumple_experiencia(self.posibilidad))
        self.posibilidad.conjunto_ofertas.agregar_oferta(self.oferta4_empresa1)
        self.assertFalse(self.empresa1.cumple_experiencia(self.posibilidad))
    
    def test_cumple_requisitos(self):
        self.posibilidad.agregar_oferta(self.oferta1_empresa1)
        self.assertTrue(self.empresa1.cumple_requisitos(self.posibilidad))
        self.posibilidad.conjunto_ofertas.agregar_oferta(self.oferta4_empresa1)
        self.assertFalse(self.empresa1.cumple_requisitos(self.posibilidad))



#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestAsociacion(unittest.TestCase):
    def setUp(self):
        self.id = 1
        self.nombre = "Asociacion 1"
        self.facturacion_media_anual_empresa1 = 1000.00
        self.facturacion_media_anual_empresa2 = 2000.00
        self.facturacion_media_anual_empresa3 = 10000.00
        self.recursos_financieros_empresa1 = 1500.00
        self.recursos_financieros_empresa2 = 2500.00
        self.recursos_financieros_empresa3 = 10000.00
        self.contrato1_empresa1 = c.Contrato(2017, 3000.00)
        self.contrato2_empresa1 = c.Contrato(2017, 4000.00)
        self.contrato1_empresa2 = c.Contrato(2017, 5000.00)
        self.contrato2_empresa2 = c.Contrato(2017, 6000.00)
        self.contratos = [self.contrato1_empresa1, self.contrato2_empresa1, self.contrato1_empresa2, self.contrato2_empresa2]
        self.empresa1 = c.Empresa(1, "Empresa 1", self.facturacion_media_anual_empresa1, self.recursos_financieros_empresa1
                                 ,[self.contrato1_empresa1, self.contrato2_empresa1])
        self.empresa2 = c.Empresa(2, "Empresa 2", self.facturacion_media_anual_empresa2, self.recursos_financieros_empresa2
                                 ,[self.contrato1_empresa2, self.contrato2_empresa2])
        self.empresa3 = c.Empresa(3, "Empresa 3", self.facturacion_media_anual_empresa3, self.recursos_financieros_empresa3
                                 ,[])
        self.asociacion = c.Asociacion(self.id, self.nombre, [self.empresa1, self.empresa2])
        self.asociacion2 = c.Asociacion(2 , "Asociacion 2", [self.empresa1, self.empresa2, self.empresa3])

    def test_atributos(self):
        self.assertEqual(self.asociacion.id, self.id)
        self.assertEqual(self.asociacion.nombre, self.nombre)
        self.assertEqual(self.asociacion.facturacion_media_anual(), self.facturacion_media_anual_empresa1 + self.facturacion_media_anual_empresa2)
        self.assertEqual(self.asociacion.recursos_financieros(), self.recursos_financieros_empresa1 + self.recursos_financieros_empresa2)
        self.assertCountEqual(self.asociacion.socios, [self.empresa1, self.empresa2])
        self.assertEqual(len(self.asociacion.contratos()), 4)
        self.assertCountEqual(self.asociacion.contratos(), self.contratos)
        self.assertIsInstance(self.asociacion.conjunto_ofertas, c.ConjuntoOfertas)
        self.assertEqual(self.asociacion.conjunto_ofertas.valor(), 0.00)
        self.assertEqual(self.asociacion.conjunto_ofertas.cantidad_ofertas(), 0)
        self.assertEqual(len(self.asociacion.adicionales), 1)
        self.assertIsInstance(self.asociacion.adicionales[0], c.AdicionalNulo)
        self.assertListEqual(self.asociacion.posibilidades, [])
    
    def test_cumple_facturacion_media_anual(self):
        self.assertTrue(self.asociacion2.cumple_facturacion_media_anual(self.facturacion_media_anual_empresa1 + self.facturacion_media_anual_empresa2 - 100))
        self.assertFalse(self.asociacion2.cumple_facturacion_media_anual(self.facturacion_media_anual_empresa1 + self.facturacion_media_anual_empresa2 + self.facturacion_media_anual_empresa3 + 100))
        self.assertFalse(self.asociacion2.cumple_facturacion_media_anual(self.facturacion_media_anual_empresa3))

    def test_cumple_facturacion_media_anual_por_socio(self):
        self.assertTrue(self.asociacion2.cumple_facturacion_media_anual_por_socio(self.facturacion_media_anual_empresa1))
        self.assertFalse(self.asociacion2.cumple_facturacion_media_anual_por_socio(self.facturacion_media_anual_empresa3))

    def test_cumple_facturacion_media_anual_un_socio(self):
        self.assertTrue(self.asociacion2.cumple_facturacion_media_anual_un_socio(self.facturacion_media_anual_empresa3 * 2.5 ))
        self.assertFalse(self.asociacion2.cumple_facturacion_media_anual_un_socio(self.facturacion_media_anual_empresa3 * 2.5 + 100))
    
    def test_cumple_recursos_financieros(self):
        self.assertTrue(self.asociacion2.cumple_recursos_financieros(self.recursos_financieros_empresa1))
        self.assertFalse(self.asociacion2.cumple_recursos_financieros(self.recursos_financieros_empresa3))
    
    def test_cumple_recursos_financieros_por_socio(self):
        self.assertTrue(self.asociacion2.cumple_recursos_financieros_por_socio(self.recursos_financieros_empresa1))
        self.assertFalse(self.asociacion2.cumple_recursos_financieros_por_socio(self.recursos_financieros_empresa3))

    def test_cumple_recursos_financieros_un_socio(self):
        self.assertTrue(self.asociacion2.cumple_recursos_financieros_un_socio(self.recursos_financieros_empresa3 * 2.5 ))
        self.assertFalse(self.asociacion2.cumple_recursos_financieros_un_socio(self.recursos_financieros_empresa3 * 2.5 + 100))


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestOferta(unittest.TestCase):
    def setUp(self):
        self.empresa = c.Empresa(1, "Empresa 1", 1000.00, 2000.00, [c.Contrato(2017, 2000)])
        self.lote = c.Lote(1, 1000.00, 2000.00, 3000.00)
        self.valor = 5000.00
        self.oferta = c.Oferta(self.empresa, self.lote, self.valor)

    def test_atributos(self):
        self.assertEqual(self.oferta.empresa, self.empresa)
        self.assertEqual(self.oferta.lote, self.lote)
        self.assertEqual(self.oferta.valor, self.valor)


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestConjuntoOfertas(unittest.TestCase):
    def setUp(self):
        self.empresa = c.Empresa(1, "Empresa 1", 1000.00, 2000.00, [c.Contrato(2017, 2000)])
        self.lote1 = c.Lote(1, 1000.00, 2000.00, 3000.00)
        self.lote2 = c.Lote(2, 1000.00, 2000.00, 3000.00)
        self.valor1 = 5000.00
        self.valor2 = 10000.00
        self.oferta1 = c.Oferta(self.empresa, self.lote1, self.valor1)
        self.oferta2 = c.Oferta(self.empresa, self.lote2, self.valor2)
        self.conjunto_ofertas = c.ConjuntoOfertas()
        self.conjunto_ofertas.agregar_oferta(self.oferta1)
        self.conjunto_ofertas.agregar_oferta(self.oferta2)

        #Aca empiezan los datos y objetos para testear los metodos
        self.lote3 = c.Lote(3, 1000.00, 2000.00, 3000.00)
        self.valor3 = 15000.00
        self.oferta3 = c.Oferta(self.empresa, self.lote3, self.valor3)
        self.conjunto_ofertas2 = c.ConjuntoOfertas()
        self.conjunto_ofertas2.agregar_oferta(self.oferta1)
        self.conjunto_ofertas2.agregar_oferta(self.oferta2)
        self.conjunto_ofertas3 = c.ConjuntoOfertas()
        self.conjunto_ofertas3.agregar_oferta(self.oferta1)
        self.conjunto_ofertas4 = c.ConjuntoOfertas()
        self.conjunto_ofertas4.agregar_oferta(self.oferta1)
        self.conjunto_ofertas4.agregar_oferta(self.oferta2)
        self.conjunto_ofertas4.agregar_oferta(self.oferta3)
        self.conjunto_ofertas5 = c.ConjuntoOfertas()
        self.conjunto_ofertas5.agregar_oferta(self.oferta3)
        

    def test_atributos(self):
        self.assertCountEqual(self.conjunto_ofertas.ofertas, set([self.oferta1, self.oferta2]))
    
    def test_agregar_oferta(self):
        self.assertNotIn(self.oferta3, self.conjunto_ofertas.ofertas)
        self.conjunto_ofertas.agregar_oferta(self.oferta3)
        self.assertIn(self.oferta3, self.conjunto_ofertas.ofertas)

    def test_quitar_oferta(self):
        self.assertIn(self.oferta2, self.conjunto_ofertas.ofertas)
        self.conjunto_ofertas.quitar_oferta(self.oferta2)
        self.assertNotIn(self.oferta2, self.conjunto_ofertas.ofertas)

    def test_lotes_ofertados(self):
        self.assertCountEqual(self.conjunto_ofertas.lotes_ofertados(), [self.lote1, self.lote2])

    def test_cantidad_ofertas(self):
        self.assertEqual(self.conjunto_ofertas.cantidad_ofertas(), 2)

    def test_oferta_contenida(self):
        self.assertTrue(self.conjunto_ofertas.oferta_contenida(self.oferta2))
        self.assertFalse(self.conjunto_ofertas.oferta_contenida(self.oferta3))

    def test_lote_contenido(self):
        self.assertTrue(self.conjunto_ofertas.lote_contenido(self.lote2))
        self.assertFalse(self.conjunto_ofertas.lote_contenido(self.lote3))

    def test_valor(self):
        self.assertEqual(self.conjunto_ofertas.valor(), self.oferta1.valor + self.oferta2.valor)

    def test_facturacion_media_anual(self):
        self.assertEqual(self.conjunto_ofertas.facturacion_media_anual(), 
                         self.oferta1.lote.facturacion_media_anual + self.oferta2.lote.facturacion_media_anual)

    def test_recursos_financieros(self):
        self.assertEqual(self.conjunto_ofertas.recursos_financieros(),
                         self.oferta1.lote.recursos_financieros + self.oferta2.lote.recursos_financieros)

    def test_experiencia(self):
        self.assertEqual(self.conjunto_ofertas.experiencia(),
                         self.oferta1.lote.experiencia + self.oferta2.lote.experiencia)

    def test_es_igual(self):
        self.assertTrue(self.conjunto_ofertas.es_igual(self.conjunto_ofertas2))
        self.assertFalse(self.conjunto_ofertas.es_igual(self.conjunto_ofertas3))
        self.assertFalse(self.conjunto_ofertas.es_igual(self.conjunto_ofertas4))

    def test_contiene(self):
        self.assertTrue(self.conjunto_ofertas.contiene(c.ConjuntoOfertas()))
        self.assertTrue(self.conjunto_ofertas.contiene(self.conjunto_ofertas2))
        self.assertTrue(self.conjunto_ofertas.contiene(self.conjunto_ofertas3))
        self.assertFalse(self.conjunto_ofertas.contiene(self.conjunto_ofertas4))

    def test_interseccion(self):
        self.assertCountEqual(self.conjunto_ofertas.interseccion(self.conjunto_ofertas3), [self.oferta1])
        self.assertCountEqual(self.conjunto_ofertas.interseccion(self.conjunto_ofertas5), [])

    def test_clonar(self):
        self.assertIsInstance(self.conjunto_ofertas.clonar(), c.ConjuntoOfertas)
        self.assertCountEqual(self.conjunto_ofertas.clonar().ofertas, self.conjunto_ofertas.ofertas)
        self.assertIsNot(self.conjunto_ofertas.clonar().ofertas, self.conjunto_ofertas.ofertas)


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestAdicional(unittest.TestCase):
    def setUp(self):
        self.empresa = c.Empresa(1, "Empresa 1", 1000.00, 2000.00, [c.Contrato(2017, 2000)])
        self.lote1 = c.Lote(1, 1000.00, 2000.00, 3000.00)
        self.lote2 = c.Lote(2, 1000.00, 2000.00, 3000.00)
        self.valor1 = 5000.00
        self.valor2 = 10000.00
        self.oferta1 = c.Oferta(self.empresa, self.lote1, self.valor1)
        self.oferta2 = c.Oferta(self.empresa, self.lote2, self.valor2)
        self.conjunto_ofertas = c.ConjuntoOfertas()
        self.conjunto_ofertas.agregar_oferta(self.oferta1)
        self.conjunto_ofertas.agregar_oferta(self.oferta2)
        self.porcentaje = -15.00
        self.adicional = c.Adicional(self.empresa, self.conjunto_ofertas, self.porcentaje)

        #Datos de la empresa
        self.facturacion_media_anual = 10000.00
        self.recursos_financieros = 20000.00
        self.valor_contrato1 = 15000.00
        self.valor_contrato2 = 12000.00
        self.valor_contrato3 = 20000.00
        self.valor_contrato4 = 40000.00
        self.contrato1 = c.Contrato(2017, self.valor_contrato1)
        self.contrato2 = c.Contrato(2017, self.valor_contrato2)
        self.contrato3 = c.Contrato(2017, self.valor_contrato3)
        self.contrato4 = c.Contrato(2017, self.valor_contrato4)
        self.contratos = [self.contrato1, self.contrato2, self.contrato3, self.contrato4]
        self.empresa1 = c.Empresa(2, "Empresa 2", self.facturacion_media_anual, self.recursos_financieros, self.contratos)

        #Valores del lote aceptado
        self.facturacion_media_anual_aceptada = 1000.00
        self.recursos_financieros_aceptados = 1500.00
        self.experiencia_aceptada = 2000.00

        #Lote aceptado por empresa 1
        self.lote1 = c.Lote(1, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_aceptada)
        self.lote1bis = c.Lote(1, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_aceptada)
        self.lote1bisbis = c.Lote(1, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_aceptada)

        #Datos de las ofertas
        self.valor_oferta = 50000.00
        self.valor_oferta2 = 60000.00
        self.oferta_aceptada = c.Oferta(self.empresa1, self.lote1, self.valor_oferta)
        self.oferta_aceptada2 = c.Oferta(self.empresa1, self.lote1bis, self.valor_oferta2)
        self.oferta_aceptada3 = c.Oferta(self.empresa1, self.lote1bisbis, self.valor_oferta2)

        #Conjuntos de ofertas
        self.conjunto_ofertas1 = c.ConjuntoOfertas()
        self.conjunto_ofertas1.agregar_oferta(self.oferta_aceptada)
        self.conjunto_ofertas1.agregar_oferta(self.oferta_aceptada2)
    
        #Datos de los Adicionales
        self.porcentaje1 = -50.00
        self.porcentaje2 = -30.00
        self.adicional_completo = c.Adicional(self.empresa1, self.conjunto_ofertas1, self.porcentaje1)

        #Datos de la posibilidad
        self.posibilidad = c.Posibilidad(self.empresa1, self.adicional_completo)

    def test_atributos(self):
        self.assertEqual(self.adicional.conjunto_ofertas, self.conjunto_ofertas)
        self.assertEqual(self.adicional.porcentaje, self.porcentaje)

    def test_esta_completo(self):
        self.assertFalse(self.adicional_completo.esta_completo(self.posibilidad))
        self.posibilidad.agregar_oferta(self.oferta_aceptada)
        self.assertFalse(self.adicional_completo.esta_completo(self.posibilidad))
        self.posibilidad.agregar_oferta(self.oferta_aceptada2)
        self.assertTrue(self.adicional_completo.esta_completo(self.posibilidad))
        self.posibilidad.agregar_oferta(self.oferta_aceptada3)
        self.assertTrue(self.adicional_completo.esta_completo(self.posibilidad))

    def test_valor(self):
        self.assertEqual(self.adicional_completo.valor(self.posibilidad), 0.00)
        self.posibilidad.agregar_oferta(self.oferta_aceptada)
        self.assertEqual(self.adicional_completo.valor(self.posibilidad), 0.00)
        self.posibilidad.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.adicional_completo.valor(self.posibilidad), 
                        (self.oferta_aceptada.valor + self.oferta_aceptada2.valor) * self.porcentaje1 / 100.00)
        self.posibilidad.agregar_oferta(self.oferta_aceptada3)
        self.assertEqual(self.adicional_completo.valor(self.posibilidad), 
                        (self.oferta_aceptada.valor + self.oferta_aceptada2.valor + self.oferta_aceptada3.valor) * self.porcentaje1 / 100.00)


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestAdicionalNulo(unittest.TestCase):
    def setUp(self):
        self.adicional_nulo = c.AdicionalNulo()

    def test_esta_completo(self):
        self.assertTrue(self.adicional_nulo.esta_completo(None))

    def test_valor(self):
        self.assertEqual(self.adicional_nulo.valor(None), 0.0)


#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestPosibilidad(unittest.TestCase):
    def setUp(self):
        self.empresa = c.Empresa(1, "Empresa 1", 1000.00, 2000.00, [c.Contrato(2017, 2000)])
        self.adicional = c.AdicionalNulo()
        self.posibilidad = c.Posibilidad(self.empresa, self.adicional)
        
        #Aca empiezan los datos y objetos para le testeo de metodos
        
        #Datos de la empresa
        self.facturacion_media_anual = 10000.00
        self.recursos_financieros = 20000.00
        self.valor_contrato1 = 15000.00
        self.valor_contrato2 = 12000.00
        self.valor_contrato3 = 20000.00
        self.contrato1 = c.Contrato(2017, self.valor_contrato1)
        self.contrato2 = c.Contrato(2017, self.valor_contrato2)
        self.contrato3 = c.Contrato(2017, self.valor_contrato3)
        self.contratos = [self.contrato1, self.contrato2, self.contrato3]
        self.empresa1 = c.Empresa(2, "Empresa 2", self.facturacion_media_anual, self.recursos_financieros, self.contratos)
        self.empresa2 = c.Empresa(2, "Empresa 2", self.facturacion_media_anual, self.recursos_financieros, [self.contrato1])

        #Datos de la posibilidad
        self.posibilidad1 = c.Posibilidad(self.empresa1, self.adicional)
        self.posibilidad2 = c.Posibilidad(self.empresa2, self.adicional)

        #Valores del lote aceptado
        self.facturacion_media_anual_aceptada = 1000.00
        self.recursos_financieros_aceptados = 1500.00
        self.experiencia_aceptada = 2000.00
        #Valores del lote rechazados
        self.facturacion_media_anual_rechazada = 15000.00
        self.recursos_financieros_rechazados = 25000.00
        self.experiencia_rechazada = 36000.00

        #Lote aceptado por empresa 1
        self.lote1 = c.Lote(1, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_aceptada)
        self.lote1bis = c.Lote(1, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_aceptada)
        #Lote rechazado por facturacion_media_anual por empresa 1
        self.lote2 = c.Lote(2, self.facturacion_media_anual_rechazada, self.recursos_financieros_aceptados, self.experiencia_aceptada)
        #Lote rechazado por recursos_financieros por empresa 1
        self.lote3 = c.Lote(3, self.facturacion_media_anual_aceptada, self.recursos_financieros_rechazados, self.experiencia_aceptada)
        #Lote rechazado por experiencia por empresa 1
        self.lote4 = c.Lote(4, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_rechazada)
        #Lote rechazado por pocos contratos por empresa 2
        self.lote5 = c.Lote(1, self.facturacion_media_anual_aceptada, self.recursos_financieros_aceptados, self.experiencia_aceptada)

        #Datos de las ofertas
        self.valor_oferta = 50000.00
        self.valor_oferta2 = 60000.00
        self.oferta_aceptada = c.Oferta(self.empresa1, self.lote1, self.valor_oferta)
        self.oferta_aceptada2 = c.Oferta(self.empresa1, self.lote1bis, self.valor_oferta2)
        self.oferta_rechazada2 = c.Oferta(self.empresa1, self.lote2, self.valor_oferta)
        self.oferta_rechazada3 = c.Oferta(self.empresa1, self.lote3, self.valor_oferta)
        self.oferta_rechazada4 = c.Oferta(self.empresa1, self.lote4, self.valor_oferta)
        self.oferta_rechazada5 = c.Oferta(self.empresa2, self.lote5, self.valor_oferta)

        #Conjuntos de ofertas
        self.conjunto_ofertas1 = c.ConjuntoOfertas()
        self.conjunto_ofertas2 = c.ConjuntoOfertas()
        self.conjunto_ofertas1.agregar_oferta(self.oferta_aceptada)
        self.conjunto_ofertas1.agregar_oferta(self.oferta_aceptada2)
        self.conjunto_ofertas2.agregar_oferta(self.oferta_aceptada)
        self.conjunto_ofertas2.agregar_oferta(self.oferta_aceptada2)
        self.conjunto_ofertas2.agregar_oferta(self.oferta_rechazada2)

    
        #Datos de los Adicionales
        self.porcentaje1 = -50.00
        self.porcentaje2 = -30.00
        self.adicional_completo = c.Adicional(self.empresa1, self.conjunto_ofertas1, self.porcentaje1)
        self.adicional_incompleto = c.Adicional(self.empresa1, self.conjunto_ofertas2, self.porcentaje2)

    def test_atributos(self):
        self.assertEqual(self.posibilidad.empresa, self.empresa)
        self.assertEqual(self.posibilidad.adicional, self.adicional)
        self.assertIsInstance(self.posibilidad.conjunto_ofertas, c.ConjuntoOfertas)
        self.assertEqual(self.posibilidad.conjunto_ofertas.cantidad_ofertas(), 0)

    def test_acepta_oferta(self):
        self.assertTrue(self.posibilidad1.acepta_oferta(self.oferta_aceptada))
        self.assertFalse(self.posibilidad1.acepta_oferta(self.oferta_rechazada2))
        self.assertFalse(self.posibilidad1.acepta_oferta(self.oferta_rechazada3))
        self.assertFalse(self.posibilidad1.acepta_oferta(self.oferta_rechazada4))
        self.assertFalse(self.posibilidad2.acepta_oferta(self.oferta_rechazada5))

    def test_agregar_oferta(self):
        self.assertCountEqual(self.posibilidad1.conjunto_ofertas.ofertas, [])
        self.posibilidad1.agregar_oferta(self.oferta_rechazada2)
        self.assertCountEqual(self.posibilidad1.conjunto_ofertas.ofertas, [])
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertCountEqual(self.posibilidad1.conjunto_ofertas.ofertas, [self.oferta_aceptada])
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertCountEqual(self.posibilidad1.conjunto_ofertas.ofertas, [self.oferta_aceptada, self.oferta_aceptada2])

    def test_adicional_completo(self):
        self.assertTrue(self.posibilidad.adicional_completo())
        self.posibilidad1 = c.Posibilidad(self.empresa1, self.adicional_completo)
        self.assertFalse(self.posibilidad1.adicional_completo())
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertFalse(self.posibilidad1.adicional_completo())
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertTrue(self.posibilidad1.adicional_completo())
        self.posibilidad1 = c.Posibilidad(self.empresa1, self.adicional_incompleto)
        self.assertFalse(self.posibilidad1.adicional_completo())
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertFalse(self.posibilidad1.adicional_completo())
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertFalse(self.posibilidad1.adicional_completo())
        self.posibilidad1.agregar_oferta(self.oferta_rechazada2)
        self.assertFalse(self.posibilidad1.adicional_completo())

    def test_lotes_ofertados(self):
        self.assertCountEqual(self.posibilidad1.lotes_ofertados(), [])
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertCountEqual(self.posibilidad1.lotes_ofertados(), [self.oferta_aceptada.lote, self.oferta_aceptada2.lote])

    def test_cantidad_lotes_ofertados(self):
        self.assertEqual(self.posibilidad1.cantidad_lotes_ofertados(), 0)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.posibilidad1.cantidad_lotes_ofertados(), 2)

    def test_oferta_contenida(self):
        self.assertFalse(self.posibilidad1.oferta_contenida(self.oferta_aceptada))
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertTrue(self.posibilidad1.oferta_contenida(self.oferta_aceptada))

    def test_lote_contenido(self):
        self.assertFalse(self.posibilidad1.lote_contenido(self.oferta_aceptada))
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertTrue(self.posibilidad1.lote_contenido(self.oferta_aceptada.lote))

    def test_valor(self):
        self.assertEqual(self.posibilidad1.valor(), 0.00)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.posibilidad1.valor(), self.oferta_aceptada.valor + self.oferta_aceptada2.valor)

    def test_valor_con_adicional(self):
        self.posibilidad1 = c.Posibilidad(self.empresa1, self.adicional_completo)
        self.assertEqual(self.posibilidad1.valor_con_adicional(), 0.00)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertEqual(self.posibilidad1.valor_con_adicional(), self.oferta_aceptada.valor)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.posibilidad1.valor_con_adicional(), (self.oferta_aceptada.valor + self.oferta_aceptada2.valor) + 
                         (self.oferta_aceptada.valor + self.oferta_aceptada2.valor) * self.porcentaje1 / 100.00 )

    def test_facturacion_media_anual(self):
        self.assertEqual(self.posibilidad1.facturacion_media_anual(), 0.00)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertEqual(self.posibilidad1.facturacion_media_anual(), self.oferta_aceptada.lote.facturacion_media_anual)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.posibilidad1.facturacion_media_anual(), self.oferta_aceptada.lote.facturacion_media_anual + 
                         self.oferta_aceptada2.lote.facturacion_media_anual)

    def test_recursos_financieros(self):
        self.assertEqual(self.posibilidad1.recursos_financieros(), 0.00)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertEqual(self.posibilidad1.recursos_financieros(), self.oferta_aceptada.lote.recursos_financieros)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.posibilidad1.recursos_financieros(), self.oferta_aceptada.lote.recursos_financieros + 
                         self.oferta_aceptada2.lote.recursos_financieros)

    def test_experiencia(self):
        self.assertEqual(self.posibilidad1.experiencia(), 0.00)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertEqual(self.posibilidad1.experiencia(), self.oferta_aceptada.lote.experiencia)
        self.posibilidad1.agregar_oferta(self.oferta_aceptada2)
        self.assertEqual(self.posibilidad1.experiencia(), self.oferta_aceptada.lote.experiencia + 
                         self.oferta_aceptada2.lote.experiencia)

    def test_clonar(self):
        self.posibilidad1.agregar_oferta(self.oferta_aceptada)
        self.assertIs(self.posibilidad1.conjunto_ofertas, self.posibilidad1.conjunto_ofertas)
        self.assertIsNot(self.posibilidad1.clonar(), self.posibilidad1)
        self.assertIsNot(self.posibilidad1.clonar().conjunto_ofertas, self.posibilidad1.conjunto_ofertas)
        self.assertIsNot(self.posibilidad1.clonar().conjunto_ofertas.ofertas, self.posibilidad1.conjunto_ofertas.ofertas)
        

#-----------------------------------------------------------------------------------------------------------------
#Listo
#-----------------------------------------------------------------------------------------------------------------
class TestCombinacion(unittest.TestCase):
    def setUp(self):
        self.empresa1 = c.Empresa(1, "Empresa 1", 10000.00, 20000.00, [c.Contrato(2017, 2000), c.Contrato(2017, 5000.00), c.Contrato(2017, 10000.00)])
        self.empresa2 = c.Empresa(2, "Empresa 2", 15000.00, 25000.00, [c.Contrato(2017, 20000), c.Contrato(2017, 50000.00), c.Contrato(2017, 100000.00)])
        self.adicional = c.AdicionalNulo()
        self.posibilidad1 = c.Posibilidad(self.empresa1, self.adicional)
        self.posibilidad2 = c.Posibilidad(self.empresa2, self.adicional)
        self.posibilidad3 = c.Posibilidad(self.empresa1, self.adicional)
        self.lote1 = c.Lote(1, 1000.00, 2000.00, 3000.00)
        self.lote2 = c.Lote(2, 1000.00, 2000.00, 3000.00)
        self.lotes = [self.lote1, self.lote2]
        self.valor1 = 1000.00
        self.valor2 = 2000.00
        self.oferta1 = c.Oferta(self.empresa1, self.lote1, self.valor1)
        self.oferta2 = c.Oferta(self.empresa2, self.lote2, self.valor2)
        self.oferta3 = c.Oferta(self.empresa1, self.lote2, self.valor2)
        self.posibilidad1.agregar_oferta(self.oferta1)
        self.posibilidad2.agregar_oferta(self.oferta2)
        self.posibilidad3.agregar_oferta(self.oferta3)
        self.combinacion1 = c.Combinacion()
        self.combinacion2 = c.Combinacion()
        self.conjunto_ofertas = c.ConjuntoOfertas()
        self.conjunto_ofertas.agregar_oferta(self.oferta1)
        self.adicional1 = c.Adicional(self.empresa1, self.conjunto_ofertas, -50)

    def test_atributos(self):
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertCountEqual(self.combinacion1.posibilidades, [self.posibilidad1, self.posibilidad2])
    
    def test_agregar_posibilidad(self):
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertCountEqual(self.combinacion1.posibilidades, [self.posibilidad1, self.posibilidad2])
        self.combinacion1.agregar_posibilidad(self.posibilidad3)
        self.assertCountEqual(self.combinacion1.posibilidades, [self.posibilidad1, self.posibilidad2])
    
    def test_acepta_posibilidad(self):
        self.assertTrue(self.combinacion1.acepta_posibilidad(self.posibilidad1))
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertFalse(self.combinacion1.acepta_posibilidad(self.posibilidad3))
    
    def test_conjunto_ofertas(self):
        self.assertCountEqual(self.combinacion1.conjunto_ofertas().ofertas, [])
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertCountEqual(self.combinacion1.conjunto_ofertas().ofertas, [self.oferta1])
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertCountEqual(self.combinacion1.conjunto_ofertas().ofertas, [self.oferta1, self.oferta2])
    
    def test_cantidad_ofertas(self):
        self.assertEqual(self.combinacion1.cantidad_ofertas(), 0)
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertEqual(self.combinacion1.cantidad_ofertas(), 1)
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertEqual(self.combinacion1.cantidad_ofertas(), 2)

    def test_lotes_ofertados(self):
        self.assertCountEqual(self.combinacion1.lotes_ofertados(), [])
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertCountEqual(self.combinacion1.lotes_ofertados(), [self.oferta1.lote])
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertCountEqual(self.combinacion1.lotes_ofertados(), [self.oferta1.lote, self.oferta2.lote])

    def test_cantidad_lotes_ofertados(self):
        self.assertEqual(self.combinacion1.cantidad_lotes_ofertados(), len([]))
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertEqual(self.combinacion1.cantidad_lotes_ofertados(), len([self.oferta1.lote]))
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertEqual(self.combinacion1.cantidad_lotes_ofertados(), len([self.oferta1.lote, self.oferta2.lote]))
    
    def test_esta_completa(self):
        self.assertFalse(self.combinacion1.esta_completa(self.lotes))
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertFalse(self.combinacion1.esta_completa(self.lotes))
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertTrue(self.combinacion1.esta_completa(self.lotes))

    def test_es_maxima(self):
        c.Combinacion.maxima = 0
        self.assertTrue(self.combinacion1.es_maxima())
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertTrue(self.combinacion1.es_maxima())
        self.assertFalse(self.combinacion2.es_maxima())
        self.combinacion2.agregar_posibilidad(self.posibilidad2)
        self.assertTrue(self.combinacion1.es_maxima())
        self.assertTrue(self.combinacion2.es_maxima())
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertTrue(self.combinacion1.es_maxima())
        self.assertFalse(self.combinacion2.es_maxima())
    
    def test_valor(self):
        self.assertEqual(self.combinacion1.valor(), 0.00)
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertEqual(self.combinacion1.valor(), self.posibilidad1.valor())
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertEqual(self.combinacion1.valor(), self.posibilidad1.valor() + self.posibilidad2.valor())
    
    def test_valor_con_adicional(self):
        self.posibilidad1.adicional = self.adicional1
        self.assertEqual(self.combinacion1.valor_con_adicional(), 0.00)
        self.combinacion1.agregar_posibilidad(self.posibilidad1)
        self.assertEqual(self.combinacion1.valor_con_adicional(), self.posibilidad1.valor_con_adicional())
        self.combinacion1.agregar_posibilidad(self.posibilidad2)
        self.assertEqual(self.combinacion1.valor_con_adicional(), self.posibilidad1.valor_con_adicional() + self.posibilidad2.valor_con_adicional())

    def test_clonar(self):
        self.assertIs(self.combinacion1.posibilidades, self.combinacion1.posibilidades)
        self.assertIsNot(self.combinacion1.clonar().posibilidades, self.combinacion1.posibilidades)
        self.assertEqual(self.combinacion1.clonar().cantidad_posibilidades(), self.combinacion1.cantidad_posibilidades())
        self.assertEqual(self.combinacion1.clonar().cantidad_lotes_ofertados(), self.combinacion1.cantidad_lotes_ofertados())


if __name__ == "__main__":
   unittest.main()
