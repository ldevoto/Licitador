from sqlite3 import connect, OperationalError, Row
from os.path import exists, isfile
from time import strftime
import clases as C
#from clases import Licitador, Lote, Empresa, Asociacion, Oferta, ConjuntoOfertas, Adicional, Contrato

def db_existente(nombre_db):
    return exists(nombre_db) and isfile(nombre_db)

def crear_db(nombre_db):
    if not db_existente(nombre_db):
        conexion = connect(nombre_db)
        cursor = conexion.cursor()
    
        try:
            cursor.execute("create table licitaciones (nombre text, fecha text)")
            conexion.commit()
        except OperationalError:
            print("Tabla Licitaciones ya creada")

        try:
            cursor.execute("create table lotes (licitacion text, id int, descripcion text, facturacion_media_anual real, recursos_financieros real, experiencia real)")
            conexion.commit()
        except OperationalError:
            print("Tabla Lotes ya creada")

        try:
            cursor.execute("create table empresas (licitacion text, id int, nombre text, facturacion_media_anual real, recursos_financieros real, asociacion int)")
            conexion.commit()
        except OperationalError:
            print("Tabla Empresas ya creada")

        try:
            cursor.execute("create table contratos (licitacion text, id_empresa int, anio int, valor real)")
            conexion.commit()
        except OperationalError:
            print("Tabla Contratos ya creada")

        try:
            cursor.execute("create table ofertas (licitacion text, id int, id_empresa int, id_lote int, valor real)")
            conexion.commit()
        except OperationalError:
            print("Tabla Ofertas ya creada")

        try:
            cursor.execute("create table conjunto_ofertas (licitacion text, id_adicional int, id_oferta int)")
            conexion.commit()
        except OperationalError:
            print("Tabla Conjunto_Ofertas ya creada")

        try:
            cursor.execute("create table adicionales (licitacion text, id int, id_empresa int, porcentaje real)")
            conexion.commit()
        except OperationalError:
            print("Tabla Adicionales ya creada")
        
        cursor.close()
        conexion.close()

def guardar_licitacion(nombre_db, licitacion, sobreescribir=False):
    nombre_licitacion = licitacion.nombre
    lotes = licitacion.lotes
    empresas = licitacion.empresas
    guardado_exitoso = True

    crear_db(nombre_db)

    conexion = connect(nombre_db)
    cursor = conexion.cursor()

    if (sobreescribir):
        cursor.execute("delete from licitaciones where nombre = ?", (nombre_licitacion,))
        cursor.execute("delete from lotes where licitacion = ?", (nombre_licitacion,))
        cursor.execute("delete from empresas where licitacion = ?", (nombre_licitacion,))
        cursor.execute("delete from contratos where licitacion = ?", (nombre_licitacion,))
        cursor.execute("delete from ofertas where licitacion = ?", (nombre_licitacion,))
        cursor.execute("delete from conjunto_ofertas where licitacion = ?", (nombre_licitacion,))
        cursor.execute("delete from adicionales where licitacion = ?", (nombre_licitacion,))

    licitacion_a_guardar = (nombre_licitacion, strftime("%d/%m/%Y"))
    cursor.execute("insert into licitaciones values (?, ?)", licitacion_a_guardar)

    lotes_a_guardar = []
    for lote in lotes:
        lotes_a_guardar.append((nombre_licitacion, ) + lote.to_registro())
    cursor.executemany("insert into lotes values (?, ?, ?, ?, ?, ?)", lotes_a_guardar)

    empresas_a_guardar = []
    for empresa in empresas:
        if empresa.es_asociacion():
            for registro in empresa.empresas_to_registro():
                empresas_a_guardar.append((nombre_licitacion, ) + registro)
        empresas_a_guardar.append((nombre_licitacion, ) + empresa.to_registro())
    cursor.executemany("insert into empresas values (?, ?, ?, ?, ?, ?)", empresas_a_guardar)

    contratos_a_guardar = []
    for empresa in empresas:
        for empresa_involucrada in empresa.empresas_involucradas():
            if not empresa_involucrada.es_asociacion():
                for contrato in empresa_involucrada.contratos():
                    contratos_a_guardar.append((nombre_licitacion, empresa_involucrada.id) + contrato.to_registro())
    cursor.executemany("insert into contratos values (?, ?, ?, ?)", contratos_a_guardar)

    ofertas_a_guardar = []
    i = 1
    for empresa in empresas:
        for oferta in empresa.conjunto_ofertas.ofertas:
            ofertas_a_guardar.append((nombre_licitacion, i) + oferta.to_registro())
            i += 1
    cursor.executemany("insert into ofertas values (?, ?, ?, ?, ?)", ofertas_a_guardar)

    conjunto_ofertas_a_guardar = []
    adicionales_a_guardar = []
    i = 1
    for empresa in empresas:
        for adicional in empresa.adicionales:
            if not adicional.es_nulo():
                id_lotes = []
                for oferta in adicional.conjunto_ofertas.ofertas:
                    id_lotes.append(oferta.lote.id)
                for registro in cursor.execute("select id from ofertas where licitacion = ? and id_empresa = ? and id_lote in ({seq})".format(seq=','.join(["?"]*len(id_lotes))), [nombre_licitacion, empresa.id] + id_lotes):
                    conjunto_ofertas_a_guardar.append((nombre_licitacion, i) + registro)
                adicionales_a_guardar.append((nombre_licitacion, i) + adicional.to_registro())
                i += 1
    cursor.executemany("insert into adicionales values (?, ?, ?, ?)", adicionales_a_guardar)
    cursor.executemany("insert into conjunto_ofertas values (?, ?, ?)", conjunto_ofertas_a_guardar)

    conexion.commit()
    #conexion.rollback()
    cursor.close()
    conexion.close()

    return guardado_exitoso


def cargar_licitacion(nombre_db, licitacion):
    nombre_licitacion = licitacion.nombre
    lotes = []
    empresas = []
    carga_exitosa = True

    crear_db(nombre_db)

    conexion = connect(nombre_db)
    conexion.row_factory = Row
    cursor = conexion.cursor()

    lotes_a_cargar = {}
    for registro in cursor.execute("select * from lotes where licitacion = ?", (nombre_licitacion,)):
        lote = C.Lote(registro["id"], registro["facturacion_media_anual"], registro["recursos_financieros"], registro["experiencia"])
        lote.descripcion = registro["descripcion"]
        lotes_a_cargar[lote.id] = lote
        #lotes_a_cargar.append({lote.id:lote})
    
    empresas_a_cargar = {}
    for registro in cursor.execute("select * from empresas where licitacion = ? and asociacion is null and facturacion_media_anual is not null and recursos_financieros is not null", (nombre_licitacion,)):
        empresa = C.Empresa(registro["id"], registro["nombre"], registro["facturacion_media_anual"], registro["recursos_financieros"], [])
        empresas_a_cargar[empresa.id] = empresa

    asociaciones_a_cargar = {}
    for registro in cursor.execute("select * from empresas where licitacion = ? and asociacion is null and facturacion_media_anual is null and recursos_financieros is null", (nombre_licitacion,)):
        asociacion = C.Asociacion(registro["id"], registro["nombre"], [])
        asociaciones_a_cargar[asociacion.id] = asociacion
    
    socios_a_cargar = {}
    for registro in cursor.execute("select * from empresas where licitacion = ? and asociacion is not null", (nombre_licitacion,)):
        socio = C.Empresa(registro["id"], registro["nombre"], registro["facturacion_media_anual"], registro["recursos_financieros"], [])
        socios_a_cargar[socio.id] = socio
        asociaciones_a_cargar[registro["asociacion"]].socios.append(socio)
    
    todas_las_subempresas = empresas_a_cargar.copy()
    todas_las_subempresas.update(socios_a_cargar)
    todas_las_empresas = empresas_a_cargar.copy()
    todas_las_empresas.update(asociaciones_a_cargar)

    for registro in cursor.execute("select * from contratos where licitacion = ?", (nombre_licitacion, )):
        contrato = C.Contrato(registro["anio"], registro["valor"])
        todas_las_subempresas[registro["id_empresa"]]._contratos.append(contrato)

    ofertas_a_cargar = {}
    for registro in cursor.execute("select * from ofertas where licitacion = ?", (nombre_licitacion,)):
        oferta = C.Oferta(todas_las_empresas[registro["id_empresa"]], lotes_a_cargar[registro["id_lote"]], registro["valor"])
        todas_las_empresas[registro["id_empresa"]].conjunto_ofertas.agregar_oferta(oferta)
        ofertas_a_cargar[registro["id"]] = oferta
    
    adicionales_a_cargar = {}
    for registro in cursor.execute("select * from adicionales where licitacion = ?", (nombre_licitacion,)):
        adicional = C.Adicional(todas_las_empresas[registro["id_empresa"]], C.ConjuntoOfertas(), registro["porcentaje"])
        todas_las_empresas[registro["id_empresa"]].agregar_adicional(adicional)
        adicionales_a_cargar[registro["id"]] = adicional
    
    for registro in cursor.execute("select * from conjunto_ofertas where licitacion = ?", (nombre_licitacion,)):
        adicionales_a_cargar[registro["id_adicional"]].conjunto_ofertas.agregar_oferta(ofertas_a_cargar[registro["id_oferta"]])

    for lote in list(lotes_a_cargar.values()):
        licitacion.agregar_lote(lote)
    
    for empresa in list(todas_las_empresas.values()):
        licitacion.agregar_empresa(empresa)

    cursor.close()
    conexion.close()
    return carga_exitosa


def obtener_licitaciones(nombre_db):
    conexion = connect(nombre_db)
    conexion.row_factory = Row
    cursor = conexion.cursor()
    licitaciones = []
    for registro in cursor.execute("select * from licitaciones order by fecha desc"):
        licitaciones.append({"nombre":registro["nombre"], "fecha":registro["fecha"]})
    cursor.close()
    conexion.close()

    return licitaciones

def eliminar_licitacion(nombre_db, licitacion):
    nombre_licitacion = licitacion.nombre
    conexion = connect(nombre_db)
    cursor = conexion.cursor()
    cursor.execute("delete from licitaciones where nombre = ?", (nombre_licitacion,))
    cursor.execute("delete from lotes where licitacion = ?", (nombre_licitacion,))
    cursor.execute("delete from empresas where licitacion = ?", (nombre_licitacion,))
    cursor.execute("delete from contratos where licitacion = ?", (nombre_licitacion,))
    cursor.execute("delete from ofertas where licitacion = ?", (nombre_licitacion,))
    cursor.execute("delete from conjunto_ofertas where licitacion = ?", (nombre_licitacion,))
    cursor.execute("delete from adicionales where licitacion = ?", (nombre_licitacion,))

    conexion.commit()
    cursor.close()
    conexion.close()


def licitacion_existente(nombre_db, nombre_licitacion):
    existe = False
    conexion = connect(nombre_db)
    cursor = conexion.cursor()
    for registro in cursor.execute("select * from licitaciones where nombre = ?", (nombre_licitacion,)):
        existe = True
        break
    cursor.close()
    conexion.close()
    return existe


def consultar_datos(nombre_db):
    conexion = connect(nombre_db)
    cursor = conexion.cursor()
    for resultado in cursor.execute("select * from licitaciones"):
        print(resultado)
    for resultado in cursor.execute("select * from lotes"):
        print(resultado)
    for resultado in cursor.execute("select * from empresas"):
        print(resultado)
    for resultado in cursor.execute("select * from contratos"):
        print(resultado)
    for resultado in cursor.execute("select * from ofertas"):
        print(resultado)
    for resultado in cursor.execute("select * from conjunto_ofertas"):
        print(resultado)
    for resultado in cursor.execute("select * from adicionales"):
        print(resultado)
    cursor.close()
    conexion.close()

def consulta_especifica(nombre_db, consulta, campos):
    conexion = connect(nombre_db)
    cursor = conexion.cursor()
    if campos != None:
        for resultado in cursor.execute(consulta, campos):
            print(resultado)
    else:
        for resultado in cursor.execute(consulta):
            print(resultado)

    conexion.close()

if __name__ == "__main__":
    '''licitacion = C.Licitador("licitacion1")
    licitacion_a_cargar = C.Licitador("licitacion1")
    lotes = [C.Lote(1, 1, 1, 1), C.Lote(2, 2.2, 2.22, 2.222), C.Lote(3, 3.3, 3.33, 3.333), C.Lote(4, 4.4, 4.44, 4.444), C.Lote(5, 5.5, 5.55, 5.555)]
    socios = [C.Empresa(100, "Empresa 100", 100, 100, [C.Contrato(2017, 100)]), C.Empresa(101, "Empresa 101", 101, 101, [C.Contrato(2017, 101)])]
    empresas = [C.Empresa(1, "Empresa 1", 1, 1, [C.Contrato(2017, 1), C.Contrato(2017, 1)]), C.Empresa(2, "Empresa 2", 2, 2, [C.Contrato(2017, 2), C.Contrato(2017, 2)]), C.Empresa(3, "Empresa 3", 3, 3, [C.Contrato(2017, 3), C.Contrato(2017, 3)]), C.Asociacion(4, "Asociacion 4",  [C.Empresa(10, "Empresa 10", 1, 1, [C.Contrato(2017, 1), C.Contrato(2017, 1)]), C.Empresa(20, "Empresa 20", 2, 2, [C.Contrato(2017, 2), C.Contrato(2017, 2)]), C.Empresa(30, "Empresa 30", 3, 3, [C.Contrato(2017, 3), C.Contrato(2017, 3)])])]
    oferta1 = C.Oferta(empresas[0], lotes[0], 12312)
    oferta2 = C.Oferta(empresas[0], lotes[1], 23434)
    oferta3 = C.Oferta(empresas[0], lotes[2], 515611)
    oferta4 = C.Oferta(empresas[0], lotes[3], 511)
    oferta5 = C.Oferta(empresas[1], lotes[0], 15)
    oferta6 = C.Oferta(empresas[1], lotes[3], 5)
    oferta7 = C.Oferta(empresas[1], lotes[2], 654)
    ofertas = [oferta1, oferta2, oferta3, oferta4, oferta5, oferta6, oferta7]
    conjunto_ofertas = C.ConjuntoOfertas()
    conjunto_ofertas.agregar_oferta(oferta1)
    conjunto_ofertas.agregar_oferta(oferta2)
    conjunto_ofertas.agregar_oferta(oferta3)
    conjunto_ofertas.agregar_oferta(oferta4)
    empresas[0].asignar_conjunto_ofertas(conjunto_ofertas)
    conjunto_ofertas2 = C.ConjuntoOfertas()
    conjunto_ofertas2.agregar_oferta(oferta5)
    conjunto_ofertas2.agregar_oferta(oferta6)
    conjunto_ofertas3 = C.ConjuntoOfertas()
    conjunto_ofertas3.agregar_oferta(oferta5)
    conjunto_ofertas3.agregar_oferta(oferta6)
    conjunto_ofertas3.agregar_oferta(oferta7)
    empresas[1].asignar_conjunto_ofertas(conjunto_ofertas3)
    adicional1 = C.Adicional(empresas[0], conjunto_ofertas, 100)
    empresas[0].agregar_adicional(adicional1)
    adicional2 = C.Adicional(empresas[1], conjunto_ofertas2, 52)
    empresas[1].agregar_adicional(adicional2)
    licitacion.lotes = lotes
    licitacion.empresas = empresas
    crear_db("Licitaciones.db")
    consultar_datos("Licitaciones.db")
    consulta_especifica("Licitaciones.db", "select id from ofertas where id in (?, ?, ?)", [1, 2, 3])
    #guardar_licitacion("Licitaciones.db", licitacion)
    cargar_licitacion("Licitaciones.db", licitacion_a_cargar)
    '''
    consulta_especifica("Licitaciones.db", "select * from adicionales where licitacion = 'Jose'", None)
