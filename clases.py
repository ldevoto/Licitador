from operator import itemgetter, attrgetter, methodcaller
import persistencia 
#from persistencia import guardar_licitacion, cargar_licitacion, db_existente

#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
    Clase encargada de almacenar toda la informacion de un lote a licitar
Atributos:
    id                         |    *   Id único del lote
    descripcion                |        Descripcion del lote
    facturacion_media_anual    |    *   Facturacion media anual requerida para licitar este lote
    recursos_financieros       |    *   Recursos financieros requeridos para licitar este lote
    experiencia                |    *   Experiencia en término de valores de contratos anteriores requerida para licitar este lote
Metodos:
'''
class Lote:
    def __init__(self, id, facturacion_media_anual, recursos_financieros, experiencia):
        self.id = id
        self.descripcion = ""
        self.facturacion_media_anual = facturacion_media_anual
        self.recursos_financieros = recursos_financieros
        self.experiencia = experiencia 
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro(self):
        return (self.id, self.descripcion, self.facturacion_media_anual, self.recursos_financieros, self.experiencia)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar(self, id, descripcion, facturacion_media_anual, recursos_financieros, experiencia):
        self.id = id
        self.descripcion = descripcion
        self.facturacion_media_anual = facturacion_media_anual
        self.recursos_financieros = recursos_financieros
        self.experiencia = experiencia
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar_de(self, lote):
        self.editar(lote.id, lote.descripcion, lote.facturacion_media_anual, lote.recursos_financieros, lote.experiencia)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        return '{{\n  "id" : {0},\n  "descripcion" : "{1}",\n  "facturacion_media_anual" : {2:.3f},\n  "recursos_financieros" : {3:.3f},\n  "experiencia" : {4:.3f}\n}}'.format(self.id, self.descripcion, self.facturacion_media_anual, self.recursos_financieros, self.experiencia)


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion:
    Clase abstracta encargada de definir un comportamiento base para todas las empresas, asociaciones, etc que 
    puedan ofertar para licitar un lote.
Atributos:
    id                      |   *   Id único de la entidad
    nombre                  |   *   Nombre de la entidad
    conjunto_ofertas        |       Conjunto de Ofertas realizadas por la entidad
    adicionales []          |   *   Array de posibles adicionales aplicado al valor por conjunto de ofertas
    posibilidades []        |       Array de posibles combinaciones segun ofertas realizadas y requisitos cumplidos
Metodos:
'''
class Entidad:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        self.conjunto_ofertas = ConjuntoOfertas()
        self.adicionales = [AdicionalNulo()]
        self.posibilidades = []

    #++++++++++++++++++
    #++++++++++++++++++
    def agregar_adicional(self, adicional):
        if not self.posee_adicional(adicional):
            self.adicionales.append(adicional)
        if not adicional.es_de_empresa(self):
            adicional.asignar_empresa(self)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def quitar_adicional(self, adicional):
        if self.posee_adicional(adicional):
            self.adicionales.remove(adicional)
        if adicional.es_de_empresa(self):
            adicional.desasignar_empresa(self)
        
    #++++++++++++++++++
    #++++++++++++++++++
    def agregar_oferta(self, oferta):
        if not self.posee_oferta(oferta):
            self.conjunto_ofertas.agregar_oferta(oferta)
        if not oferta.es_de_empresa(self):
            oferta.asignar_empresa(self)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def quitar_oferta(self, oferta):
        if self.posee_oferta(oferta):
            self.conjunto_ofertas.quitar_oferta(oferta)
        if oferta.es_de_empresa(self):
            oferta.desasignar_empresa(self)

    #++++++++++++++++++
    #++++++++++++++++++
    def agregar_conjunto_ofertas(self, conjunto_ofertas):
        for oferta in conjunto_ofertas.ofertas:
            self.agregar_oferta(oferta)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def quitar_conjunto_ofertas(self, conjunto_ofertas):
        for oferta in conjunto_ofertas.ofertas:
            self.quitar_oferta(oferta)
        
    #++++++++++++++++++
    #++++++++++++++++++
    def quitar_todas_las_ofertas(self):
        ofertas = list(self.conjunto_ofertas.ofertas)
        for oferta in ofertas:
            self.quitar_oferta(oferta)
        
    #++++++++++++++++++
    #++++++++++++++++++
    def quitar_todos_los_adicionales(self):
        adicionales = [adicional for adicional in self.adicionales if not adicional.es_nulo()]
        for adicional in adicionales:
            self.quitar_adicional(adicional)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def posee_oferta(self, oferta):
        return self.conjunto_ofertas.oferta_contenida(oferta)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def posee_adicional(self, adicional):
        return adicional in self.adicionales
    
    #++++++++++++++++++
    #++++++++++++++++++
    def pasar_ofertas_y_adicionales_a_empresa(self, empresa):
        ofertas = list(self.conjunto_ofertas.ofertas)
        for oferta in ofertas:
            oferta.asignar_empresa(empresa)
        adicionales = [adicional for adicional in self.adicionales if not adicional.es_nulo()]
        for adicional in adicionales:
            adicional.asignar_empresa(empresa)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def eliminar(self):
        self.quitar_todas_las_ofertas()
        self.quitar_todos_los_adicionales()

    def calcular_posibilidades(self):
        for adicional in self.adicionales:
            self._generar_posibilidades(Posibilidad(self, adicional), self.conjunto_ofertas.ofertas)

    def _generar_posibilidades(self, posibilidad, ofertas):
        ofertas_usadas = set()
        for oferta in ofertas:
            ofertas_usadas.add(oferta)
            if posibilidad.acepta_oferta(oferta):
                posibilidad_clonada = posibilidad.clonar()
                posibilidad_clonada.agregar_oferta(oferta)
                if posibilidad_clonada.adicional_completo():
                    self.posibilidades.append(posibilidad_clonada)
                self._generar_posibilidades(posibilidad_clonada, ofertas - ofertas_usadas)

    def lotes_ofertados(self):
        return self.conjunto_ofertas.lotes_ofertados()

    def cantidad_lotes_ofertados(self):
        return self.conjunto_ofertas.cantidad_ofertas()

    def facturacion_media_anual(self):
        return 0.0

    def recursos_financieros(self):
        return 0.0

    def contratos(self):
        return []

    def cantidad_contratos(self):
        return len(self.contratos())

    def experiencia(self, posibilidad):
        if self.contratos():
            return sum(contrato.valor for contrato in self.contratos()[:posibilidad.cantidad_lotes_ofertados() + 1])
            #return sum(contrato.valor for contrato in self.contratos())
        else:
            return 0.0

    def cumple_facturacion_media_anual(self, facturacion_media_anual):
        return self.facturacion_media_anual() >= facturacion_media_anual

    def cumple_recursos_financieros(self, recursos_financieros):
        return self.recursos_financieros() >= recursos_financieros

    def cumple_experiencia(self, posibilidad):
        return  self.cantidad_contratos() > posibilidad.cantidad_lotes_ofertados() and self.experiencia(posibilidad) >= posibilidad.experiencia()

    def cumple_requisitos(self, posibilidad):
        return (self.cumple_facturacion_media_anual(posibilidad.facturacion_media_anual())
        and self.cumple_recursos_financieros(posibilidad.recursos_financieros()) 
        and self.cumple_experiencia(posibilidad))
    
    #++++++++++++++++++
    #++++++++++++++++++
    def empresas_involucradas(self):
        return [self]
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_asociacion(self):
        return False

    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro(self):
        return self.to_registro_sin_padre() + (None, )
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro_sin_padre(self):
        return (self.id, self.nombre, self.facturacion_media_anual(), self.recursos_financieros())
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar(self, id, nombre):
        self.id = id
        self.nombre = nombre
    

#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion:
Atributos Heredados:
    id                          |   *
    nombre                      |   *
    conjunto_ofertas            |   
    posibilidades []            |   
Atributos:
    _facturacion_media_anual    |   *   Facturacion media anual de la empresa
    _recursos_financieros       |   *   Recursos financieros con los que cuenta la empresa
    _contratos []               |   *   Contratos cumplidos anteriormente por la empresa
Metodos:
'''
class Empresa(Entidad):
    def __init__(self, id, nombre, facturacion_media_anual, recursos_financieros, contratos):
        Entidad.__init__(self, id, nombre)
        self._facturacion_media_anual = facturacion_media_anual
        self._recursos_financieros = recursos_financieros
        self._contratos = sorted(contratos, key=attrgetter("valor"), reverse=True)

    def facturacion_media_anual(self):
        return self._facturacion_media_anual

    def recursos_financieros(self):
        return self._recursos_financieros

    def contratos(self):
        return self._contratos
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar(self, id, nombre, facturacion_media_anual, recursos_financieros, contratos):
        super().editar(id, nombre)
        self._facturacion_media_anual = facturacion_media_anual
        self._recursos_financieros = recursos_financieros
        self._contratos = contratos
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar_de(self, empresa):
        self.editar(empresa.id, empresa.nombre, empresa.facturacion_media_anual(), empresa.recursos_financieros(), empresa.contratos())

    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        json = ""
        for contrato in self.contratos():
            json += "    " + contrato.to_json().replace("\n", "\n    ") + ",\n"
        json = json[:-2:]
        return '{{\n  "id" : {0},\n  "nombre" : "{1}",\n  "facturacion_media_anual" : {2:.3f},\n  "recursos_financieros" : {3:.3f},\n  "contratos" : \n  [\n{4}\n  ]\n}}'.format(self.id, self.nombre, self.facturacion_media_anual(), self.recursos_financieros(), json)

    
#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion:
Atributos Heredados:
    id                      |   *
    nombre                  |   *
    conjunto_ofertas        |   *
    posibilidades []        |   
Atributos:
    socios []               |   *   Array de socios que conforman la asociacion
Metodos:
'''
class Asociacion(Entidad):
    def __init__(self, id, nombre, socios):
        Entidad.__init__(self, id, nombre)
        self.socios = socios

    def facturacion_media_anual(self):
        return sum(socio.facturacion_media_anual() for socio in self.socios)

    def recursos_financieros(self):
        return sum(socio.recursos_financieros() for socio in self.socios)

    def contratos(self):
        return sorted(list(set.union(*[set(socio.contratos()) for socio in self.socios])), key=attrgetter("valor"), reverse=True)

    def cumple_facturacion_media_anual(self, facturacion_media_anual):
        return (super(Asociacion, self).cumple_facturacion_media_anual(facturacion_media_anual)
           and self.cumple_facturacion_media_anual_por_socio(facturacion_media_anual)
           and self.cumple_facturacion_media_anual_un_socio(facturacion_media_anual))

    def cumple_facturacion_media_anual_por_socio(self, facturacion_media_anual):
        entro = False
        cumple = True
        for socio in self.socios:
            if not socio.cumple_facturacion_media_anual(facturacion_media_anual * 0.2):
                if entro:
                    cumple = False
                    break
                else:
                    if socio.cumple_facturacion_media_anual(facturacion_media_anual * 0.15):
                        entro = True
                    else:
                        cumple = False
                        break
        return cumple

    def cumple_facturacion_media_anual_un_socio(self, facturacion_media_anual):
        return any(socio.cumple_facturacion_media_anual(facturacion_media_anual * 0.4) for socio in self.socios)

    def cumple_recursos_financieros(self, recursos_financieros):
        return (super(Asociacion, self).cumple_recursos_financieros(recursos_financieros)
           and self.cumple_recursos_financieros_por_socio(recursos_financieros)
           and self.cumple_recursos_financieros_un_socio(recursos_financieros))

    def cumple_recursos_financieros_por_socio(self, recursos_financieros):
        return all(socio.cumple_recursos_financieros(recursos_financieros * 0.25) for socio in self.socios)

    def cumple_recursos_financieros_un_socio(self, recursos_financieros):
        return any(socio.cumple_recursos_financieros(recursos_financieros * 0.4) for socio in self.socios)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def empresas_involucradas(self):
        return [self] + self.socios
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_asociacion(self):
        return True
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro_sin_padre(self):
        return (self.id, self.nombre, None, None)

    #++++++++++++++++++
    #++++++++++++++++++
    def empresas_to_registro(self):
        return [socio.to_registro_sin_padre() + (self.id, ) for socio in self.socios]
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar(self, id, nombre, socios):
        super().editar(id, nombre)
        self.socios = socios
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar_de(self, asociacion):
        self.editar(asociacion.id, asociacion.nombre, asociacion.socios)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        json = ""
        for socio in self.socios:
            json += "    " + socio.to_json().replace("\n", "\n    ") + ",\n"
        json = json[:-2:]
        return '{{\n  "id" : {0},\n  "nombre" : "{1}",\n  "socios" : \n  [\n{2}\n  ]\n}}'.format(self.id, self.nombre, json)


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion:
    Clase que contiene una posible combinacion de ofertas para una determinada empresa. Puede contener descuento o no
Atributos:
    empresa                 |   *   Nombre de la empresa a la que corresponde la posibilidad
    conjunto_ofertas        |       Conjunto de Ofertas por las que está compuesta la posibilidad
    adicional               |   *   Adicional por el que esta compuesta la posibilidad (Adicional_Nulo o Descuento)
Metodos:

'''
class Posibilidad:
    def __init__(self, empresa, adicional):
        self.empresa = empresa
        self.conjunto_ofertas = ConjuntoOfertas()
        self.adicional = adicional

    def acepta_oferta(self, oferta):
        self.conjunto_ofertas.agregar_oferta(oferta)
        aceptacion = self.empresa.cumple_requisitos(self)
        self.conjunto_ofertas.quitar_oferta(oferta)
        return aceptacion
            
    def agregar_oferta(self, oferta):
        if self.acepta_oferta(oferta):
            self.conjunto_ofertas.agregar_oferta(oferta)

    def adicional_completo(self):
        return self.adicional.esta_completo(self)

    def lotes_ofertados(self):
        return self.conjunto_ofertas.lotes_ofertados()

    def cantidad_lotes_ofertados(self):
        return self.conjunto_ofertas.cantidad_ofertas()

    def oferta_contenida(self, oferta):
        return self.conjunto_ofertas.oferta_contenida(oferta)

    def lote_contenido(self, lote):
        return self.conjunto_ofertas.lote_contenido(lote)

    def valor(self):
        return self.conjunto_ofertas.valor()

    def valor_con_adicional(self):
        return self.conjunto_ofertas.valor() + self.adicional.valor(self)

    def facturacion_media_anual(self):
        return self.conjunto_ofertas.facturacion_media_anual()

    def recursos_financieros(self):
        return self.conjunto_ofertas.recursos_financieros()

    def experiencia(self):
        return self.conjunto_ofertas.experiencia()

    def clonar(self):
        posibilidad = Posibilidad(self.empresa, self.adicional)
        posibilidad.conjunto_ofertas = self.conjunto_ofertas.clonar()
        return posibilidad
    
    def to_json(self, con_valores=True):
        json_ofertas = self.conjunto_ofertas.to_json().replace("\n", "\n    ")
        json_adicional = self.adicional.to_json().replace("\n", "\n    ")
        if con_valores:
            return '{{\n  "empresa" : {0},\n  "valor" : {1:.3f},\n  "valor_con_adicional" : {2:.3f},\n  "ofertas" :\n    {3},\n  "adicional" : \n    {4}\n}}'.format(self.empresa.id, self.valor(), self.valor_con_adicional(), json_ofertas, json_adicional)
        else:
            return '{{\n  "empresa" : {0},\n  "ofertas" :\n    {1},\n  "adicional" : \n    {2}\n}}'.format(self.empresa.id, json_ofertas, json_adicional)
        


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
Atributos:
    empresa     |   *   Empresa a la que pertenece la oferta
    lote        |   *   Lote perteneciente a la oferta
    valor       |   *   Valor de la oferta
Metodos: 

'''
class Oferta:
    def __init__(self, empresa, lote, valor, efectiva=True):
        self.empresa = None
        self.lote = lote
        self.valor = valor
        if efectiva:
            self.asignar_empresa(empresa)
        else:
            self.empresa = empresa
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_equivalente(self, oferta):
        return (self.lote == oferta.lote and self.empresa == oferta.empresa)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro(self):
        return (self.empresa.id, self.lote.id, self.valor)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_de_empresa(self, empresa):
        return self.empresa == empresa
    
    #++++++++++++++++++
    #++++++++++++++++++
    def asignar_empresa(self, empresa):
        if self.empresa != empresa:
            if self.empresa != None:
                self.empresa.quitar_oferta(self)
            self.empresa = empresa
        if not empresa.posee_oferta(self):
            empresa.agregar_oferta(self)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def desasignar_empresa(self, empresa):
        if self.empresa == empresa:
            self.empresa = None
        if empresa.posee_oferta(self):
            empresa.quitar_oferta(self)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def eliminar(self):
        if self.empresa != None:
            self.desasignar_empresa(self.empresa)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar(self, empresa, lote, valor):
        self.asignar_empresa(empresa)
        self.lote = lote
        self.valor = valor
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar_de(self, oferta):
        self.editar(oferta.empresa, oferta.lote, oferta.valor)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        return '{{\n  "empresa" : {0},\n  "lote" : {1},\n  "valor" : {2:.3f}\n}}'.format(self.empresa.id, self.lote.id, self.valor)


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion:
    Clase contenedora de Ofertas. Existe para definir comportamiento de un grupo de Ofertas.
Atributos:
    ofertas set()       |       Conjunto de ofertas contenidas por el conjunto
Metodos: 

'''
class ConjuntoOfertas:
    def __init__(self):
        self.ofertas = set()

    def agregar_oferta(self, oferta):
        self.ofertas.add(oferta)

    def quitar_oferta(self, oferta):
        self.ofertas.remove(oferta)

    def lotes_ofertados(self):
        return [oferta.lote for oferta in self.ofertas]

    def cantidad_ofertas(self):
        return len(self.ofertas)

    def oferta_contenida(self, oferta):
        return oferta in self.ofertas
    
    #++++++++++++++++++
    #++++++++++++++++++
    def oferta_existente(self, oferta):
        return any(oferta.es_equivalente(oferta1) for oferta1 in self.ofertas)

    def lote_contenido(self, lote):
        return lote in self.lotes_ofertados()

    def valor(self):
        return sum(oferta.valor for oferta in self.ofertas)

    def facturacion_media_anual(self):
        return sum(lote.facturacion_media_anual for lote in self.lotes_ofertados())

    def recursos_financieros(self):
        return sum(lote.recursos_financieros for lote in self.lotes_ofertados())

    def experiencia(self):
        return sum(lote.experiencia for lote in self.lotes_ofertados())

    def es_igual(self, conjunto_ofertas):
        return self.ofertas == conjunto_ofertas.ofertas
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_equivalente(self, conjunto_ofertas):
        return self.cantidad_ofertas() == conjunto_ofertas.cantidad_ofertas() and all(any(oferta1.es_equivalente(oferta) for oferta in self.ofertas) for oferta1 in conjunto_ofertas.ofertas)

    def contiene(self, conjunto_ofertas):
        return self.ofertas.issuperset(conjunto_ofertas.ofertas)

    def interseccion(self, conjunto_ofertas):
        return self.ofertas.intersection(conjunto_ofertas.ofertas)

    def clonar(self):
        conjunto_ofertas = ConjuntoOfertas()
        conjunto_ofertas.ofertas = set(self.ofertas)
        return conjunto_ofertas
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro(self):
        return [(oferta.id,) for oferta in self.ofertas]
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        json = ""
        for oferta in self.ofertas:
            json += "  " + oferta.to_json().replace("\n", "\n  ") + ",\n"
        json = json[:-2:]
        return '[\n{0}\n]'.format(json)


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
Atributos:
Metodos: 

'''
class Adicional:
    def __init__(self, empresa, conjunto_ofertas, porcentaje, efectiva=True):
        self.empresa = None
        self.conjunto_ofertas = conjunto_ofertas
        self.porcentaje = porcentaje
        if efectiva:
            self.asignar_empresa(empresa)
        else:
            self.empresa = empresa

    def esta_completo(self, posibilidad):
        return posibilidad.conjunto_ofertas.contiene(self.conjunto_ofertas)

    def valor(self, posibilidad):
        if self.esta_completo(posibilidad):
            valor = posibilidad.valor() * self.porcentaje / 100.0
        else:
            valor = 0.0
        return valor
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_equivalente(self, adicional):
        return (self.conjunto_ofertas.es_equivalente(adicional.conjunto_ofertas))
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro(self):
        return (self.empresa.id, self.porcentaje)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_nulo(self):
        return False
    
    #++++++++++++++++++
    #++++++++++++++++++
    def asignar_empresa(self, empresa):
        if self.empresa != empresa:
            if self.empresa != None:
                self.empresa.quitar_adicional(self)
            self.empresa = empresa
        if not empresa.posee_adicional(self):
            empresa.agregar_adicional(self)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def desasignar_empresa(self, empresa):
        if self.empresa == empresa:
            self.empresa = None
        if empresa.posee_adicional(self):
            empresa.quitar_adicional(self)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def es_de_empresa(self, empresa):
        return self.empresa == empresa
    
    #++++++++++++++++++
    #++++++++++++++++++
    def eliminar(self):
        if self.empresa != None:
            self.desasignar_empresa(self.empresa)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def editar(self, empresa, conjunto_ofertas, porcentaje):
        self.asignar_empresa(empresa)
        self.conjunto_ofertas = conjunto_ofertas
        self.porcentaje = porcentaje

    #++++++++++++++++++
    #++++++++++++++++++
    def editar_de(self, adicional):
        self.editar(adicional.empresa, adicional.conjunto_ofertas, adicional.porcentaje)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        json_ofertas = self.conjunto_ofertas.to_json().replace("\n", "\n    ")
        return '{{\n  "empresa" : {0},\n  "porcentaje" : {1:.3f},\n  "ofertas" : \n    {2}\n}}'.format(self.empresa.id, self.porcentaje, json_ofertas)

#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
Atributos:
Metodos: 

'''
class AdicionalNulo:
    def __init__(self):
        pass

    def esta_completo(self, posibilidad):
        return True

    def valor(self, posibilidad):
        return 0.0

    #++++++++++++++++++
    #++++++++++++++++++
    def es_nulo(self):
        return True
    
    def to_json(self):
        return '{\n  "empresa" : null,\n  "ofertas" : null,\n  "porcentaje" : 0.000\n}'

#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
Atributos:
Metodos: 

'''
class Contrato:
    def __init__(self, anio, valor):
        self.anio = anio
        self.valor = valor
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_registro(self):
        return (self.anio, self.valor)
    
    #++++++++++++++++++
    #++++++++++++++++++
    def to_json(self):
        return '{{\n  "anio" : {0},\n  "valor" : {1:.3f}\n}}'.format(self.anio, self.valor)


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
Atributos:
    posibilidades []        |       Array de posibilidade por las que está compuesta la combinacion
Metodos: 

'''
class Combinacion:
    maxima = 0
    def __init__(self):
        self.posibilidades = []

    def agregar_posibilidad(self, posibilidad):
        if self.acepta_posibilidad(posibilidad):
            self.posibilidades.append(posibilidad)
            if self.cantidad_ofertas() > Combinacion.maxima:
                Combinacion.maxima = self.cantidad_ofertas()

    def acepta_posibilidad(self, posibilidad):
        return not set(self.conjunto_ofertas().lotes_ofertados()).intersection(set(posibilidad.conjunto_ofertas.lotes_ofertados()))

    def conjunto_ofertas(self):
        conjunto_ofertas = ConjuntoOfertas()
        if self.cantidad_posibilidades() != 0:
            for oferta in set.union(*[posibilidad.conjunto_ofertas.ofertas for posibilidad in self.posibilidades]):
                conjunto_ofertas.agregar_oferta(oferta)
        return conjunto_ofertas

    def cantidad_ofertas(self):
        return self.conjunto_ofertas().cantidad_ofertas()
    
    def cantidad_posibilidades(self):
        return len(self.posibilidades)

    def lotes_ofertados(self):
        if self.cantidad_posibilidades() != 0:
            return list(set.union(*[set(posibilidad.conjunto_ofertas.lotes_ofertados()) for posibilidad in self.posibilidades]))
        else:
            return []

    def cantidad_lotes_ofertados(self):
        return len(self.lotes_ofertados())

    def esta_completa(self, lotes):
        return self.cantidad_ofertas() == len(lotes)

    def es_maxima(self):
        return self.cantidad_ofertas() == Combinacion.maxima

    def valor(self):
        return sum(posibilidad.valor() for posibilidad in self.posibilidades)

    def valor_con_adicional(self):
        return sum(posibilidad.valor_con_adicional() for posibilidad in self.posibilidades)

    def clonar(self):
        combinacion = Combinacion()
        combinacion.posibilidades = list(self.posibilidades)
        return combinacion
    
    def to_json(self, con_valores=True):
        json = ""
        for posibilidad in self.posibilidades:
            json += "      " + posibilidad.to_json().replace("\n", "\n      ") + ",\n"
        json = json[:-2:]
        if con_valores:
            return '{{\n  "valor" : {0:.3f},\n  "valor_con_adicional" : {1:.3f},\n  "posibilidades" : \n    [\n{2}\n    ]\n}}'.format(self.valor(), self.valor_con_adicional(), json)
        else:
            return '{{\n  "posibilidades" : \n    [\n{0}\n    ]\n}}'.format(json)


#----------------------------------------------------------------------------------------------------------------------------------------------

'''
Descripcion: 
Atributos:
Metodos: 
'''
class Licitador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.lotes = []
        self.empresas = set()
        self.combinaciones = []

    def agregar_lote(self, lote):
        self.lotes.append(lote)
    
    def agregar_empresa(self, empresa):
        self.empresas.add(empresa)
    
    def agregar_combinacion(self, combinacion):
        self.combinaciones.append(combinacion)
    
    def iniciar_licitacion(self):
        self.calcular_posibilidades_empresas()
        self.calcular_combinaciones()
    
    def calcular_posibilidades_empresas(self):
        for empresa in self.empresas:
            empresa.calcular_posibilidades()
    
    def calcular_combinaciones(self):
        self._generar_combinaciones(Combinacion(), self.empresas)
    
    def _generar_combinaciones(self, combinacion, empresas):
        empresas_usadas = set()
        for empresa in empresas:
            empresas_usadas.add(empresa)
            for posibilidad in empresa.posibilidades:
                if combinacion.acepta_posibilidad(posibilidad):
                    combinacion_clonada = combinacion.clonar()
                    combinacion_clonada.agregar_posibilidad(posibilidad)
                    self.agregar_combinacion(combinacion_clonada)
                    if not combinacion_clonada.esta_completa(self.lotes):
                        self._generar_combinaciones(combinacion_clonada, empresas - empresas_usadas)
    
    def reducir_combinaciones(self):
        combinaciones = []
        for combinacion in self.combinaciones:
            if combinacion.es_maxima():
                combinaciones.append(combinacion)
        self.combinaciones = combinaciones
    
    def ordenar_combinaciones(self):
        self.combinaciones = sorted(self.combinaciones, key=methodcaller("valor_con_adicional"))
    
    def combinacion_ganadora(self):
        return min(self.combinaciones, key=methodcaller("valor_con_adicional"))
    
    def guardar_licitacion(self):
        print(persistencia.guardar_licitacion("Licitaciones.db", self))
    
    def cargar_licitacion(self):
        print(persistencia.cargar_licitacion("Licitaciones.db", self))
    
    def sobreescribir_licitacion(self):
        print(persistencia.guardar_licitacion("Licitaciones.db", self, sobreescribir=True))



#----------------------------------------------------------------------------------------------------------------------------------------------
