from clases import *

empresa1 = Empresa(1, "empresa 1", 1, 1, [])
empresa2 = Empresa(2, "empresa 2", 2, 2, [])
lote = Lote(1, 1, 1, 1)
oferta1 = Oferta(empresa1, lote, 1)
oferta2 = Oferta(empresa2, lote, 2)
adicional1 = Adicional(empresa1, ConjuntoOfertas(), 1)
adicional2 = Adicional(empresa2, ConjuntoOfertas(), 2)

empresa1.quitar_oferta(oferta1)
empresa1.agregar_oferta(oferta2)
empresa2.quitar_adicional(adicional2)
empresa2.agregar_adicional(adicional1)

empresa1.agregar_oferta(oferta1)
empresa1.agregar_oferta(oferta2)
empresa2.agregar_oferta(oferta1)
empresa2.agregar_oferta(oferta2)

empresa1.agregar_adicional(adicional1)
empresa1.agregar_adicional(adicional2)
empresa2.agregar_adicional(adicional1)
empresa2.agregar_adicional(adicional2)

empresa1.quitar_oferta(oferta1)
empresa1.quitar_oferta(oferta2)
empresa2.quitar_oferta(oferta1)
empresa2.quitar_oferta(oferta2)

empresa1.quitar_adicional(adicional1)
empresa1.quitar_adicional(adicional2)
empresa2.quitar_adicional(adicional1)
empresa2.quitar_adicional(adicional2)

oferta1.asignar_empresa(empresa1)
oferta1.asignar_empresa(empresa2)
oferta2.asignar_empresa(empresa1)
oferta2.asignar_empresa(empresa2)

adicional1.asignar_empresa(empresa1)
adicional1.asignar_empresa(empresa2)
adicional2.asignar_empresa(empresa1)
adicional2.asignar_empresa(empresa2)

oferta1.desasignar_empresa(empresa1)
oferta1.desasignar_empresa(empresa2)
oferta2.desasignar_empresa(empresa1)
oferta2.desasignar_empresa(empresa2)

adicional1.desasignar_empresa(empresa1)
adicional1.desasignar_empresa(empresa2)
adicional2.desasignar_empresa(empresa1)
adicional2.desasignar_empresa(empresa2)
