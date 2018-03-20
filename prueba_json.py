from clases import *
lote1 = Lote(1, 111, 1111, 1111)
lote1.descripcion = "Lote 1"
lote2 = Lote(2, 222, 2222, 2222)
lote2.descripcion = "Lote 2"
lote3 = Lote(3, 333, 3333, 3333)
lote3.descripcion = "Lote 3"
empresa1 = Empresa(1, "Empresa 1", 1111, 1111, [Contrato(2017, 11), Contrato(2017, 12)])
empresa2 = Empresa(2, "Empresa 2", 2222, 2222, [Contrato(2017, 21), Contrato(2017, 22)])
asociacion1 = Asociacion(3, "Asociacion 3", [empresa1, empresa2])
oferta11 = Oferta(empresa1, lote1, 11)
oferta12 = Oferta(empresa1, lote2, 12)
oferta13 = Oferta(empresa1, lote3, 13)
conjunto_ofertas1 = ConjuntoOfertas()
conjunto_ofertas1.agregar_oferta(oferta11)
conjunto_ofertas1.agregar_oferta(oferta12)
conjunto_ofertas1.agregar_oferta(oferta13)
adicional1 = Adicional(empresa1, conjunto_ofertas1, -10)
adicional_nulo = AdicionalNulo()
posibilidad1 = Posibilidad(empresa1, adicional1)
posibilidad1.conjunto_ofertas = conjunto_ofertas1
posibilidad2 = Posibilidad(empresa1, adicional_nulo)
posibilidad2.conjunto_ofertas = conjunto_ofertas1
combinacion1 = Combinacion()
combinacion1.posibilidades.append(posibilidad1)
combinacion1.posibilidades.append(posibilidad2)
