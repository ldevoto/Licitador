# LicitaSoft
## LicitaSoft es un aplicativo que determina la mejor combinación de oferentes según una serie de lotes dados para licitar.
### Información de entrada (Input):
- Lotes
- Entidades (Empresas o Asociaciones)
- Ofertas (realizadas por Entidades sobre Lotes)
- Descuentos (ofrecidos por Entidades sobre un conjunto de Lotes si es adjudicado)
### Información de salida (Output):
- Combinacion ganadora (de Ofertas considerando descuentos)
- Combinaciones probadas (de Ofertas (todas, con/sin descuentos))

## El proceso completo para la determinación de la combinación ganadora se puede divir en 3 grandes etapas:
1. Carga de datos
2. Cálculo de combinaciones
3. Determinación del ganador y muestra de datos

A continuación se explica brevemente cada una de las etapas con más detalle
## 1. Carga de datos
En la carga de datos sucede todo lo correspondiente al input de información.
En esta etapa se presentan pantallas claramente diferenciadas para el ingreso de Lotes, Entidades, Ofertas y Descuentos, de las cuales se solicita información específica
- Lotes:
  - Id
  - Descripción
  - Facturación media anual requerida
  - Recursos financieros requeridos
  - Experiencia requerida
- Entidades (Existen dos tipos):
  - Empresas:
    - Id
    - Nombre
    - Facturación media anual declarada
    - Recursos financieros disponibles
    - Contratos concretados anteriormente
      - Año del contrato
      - Valor del contrato
  - Asociaciones:
    - Id
    - Nombre
    - Socios (Conjunto de Empresas. Se ingresan igual que las Empresas)
- Ofertas:
  - Entidad (Según las ingresadas)
  - Lote (Según los ingresados)
  - Valor
- Descuentos:
  - Lotes (Según los ingresados)
  - Entidad (Según las ingresadas)
  - Porcentaje 
