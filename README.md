# LicitaSoft
## LicitaSoft es un aplicativo que determina la mejor combinación de oferentes según una serie de lotes dados para licitar.

### Información de entrada (Input):
- Lotes
- Entidades (Empresas o Asociaciones)
- Ofertas (realizadas por Entidades sobre Lotes)
- Descuentos (ofrecidos por Entidades sobre un conjunto de Lotes si es adjudicado)

### Información de salida (Output):
- Combinación ganadora (de Ofertas considerando descuentos)
- Combinaciones probadas (de Ofertas (todas, con/sin descuentos))

## El proceso completo para la determinación de la combinación ganadora se puede divir en 3 grandes etapas:
1. Carga de datos
2. Cálculo de combinaciones
3. Determinación del ganador y muestra de datos

A continuación se explica brevemente cada una de las etapas con más detalle

## 1. Carga de datos
En la carga de datos sucede todo lo correspondiente al input de información.
En esta etapa se presentan pantallas claramente diferenciadas para el ingreso de Lotes, Entidades, Ofertas y Descuentos, de las cuales se solicita información específica.
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
  
 Los datos solicitados son conservados, preparados y relacionados apropiadamente para dar paso a la etapa 2.

## 2. Cálculo de combinaciones
En esta etapa ocurren todos los cálculos necesarios para determinar que combinaciones van a ser factibles y generarlas para posterior trabajo con ellas. A grandes rasgos esta etapa se encarga de determinar que Posibilidades de ofertas son posibles, según el criterio de riesgo y seleccón, para cada Entidad. Una vez determinadas las Posibilidades para cada Entidad, se procede a combinar dichas posibilidades y generar las combinaciones finales. Estos pasos pueden verse un poco más detallados a continuación
### 1. Generación de Posibilidades para cada Entidad.
  - Una Posibilidad es una posible combinación de ofertas para una Entidad en particular. Una Entidad puede ofertar 1 o más Lotes por lo que hay que determinar todas las combinaciones posibles con esas ofertas. Para hacerlo se tienen en cuenta los [criterios de riesgo y selección](https://github.com/ldevoto/Licitador#criterios-de-riesgo-y-selecci%C3%B3n-de-ofertentes). Por ejemplo una Entidad podría ofertar 3 Lotes dándonos 2&sup3; = 8 posibles combinaciones de Oferta para esa Entidad. Una adjudicándole sólo el primer Lote, otra sólo el segundo, otra sólo el tercero, otra con los dos primeros, etc. Así hasta terminar todas las posibilidades   De esas 8 ofertas tal vez haya alguna que no cumpla con los criterios y queden descartadas de antemano. Este proceso se realiza para todas las Entidades ingresadas sobre todas las Ofertas que hayan hecho.
  - 
  
# Criterios de Riesgo y Selección de Ofertentes
