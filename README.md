# LicitaSoft
## LicitaSoft es un aplicativo (_escito en Python y orientado a objetos_) que determina la mejor combinación de oferentes según una serie de lotes dados para licitar

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

A continuación se explica cada una de las etapas con más detalle

### 1. Carga de datos
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

### 2. Cálculo de combinaciones
Aquí ocurren todos los cálculos necesarios para determinar que combinaciones van a ser factibles y generarlas para posterior trabajo con ellas. A grandes rasgos esta etapa se encarga de determinar que Posibilidades de ofertas son posibles, según un [criterio de riesgo y seleccón](#análisis-de-riesgo-y-criterio-de-selección-de-oferentes), para cada Entidad. Una vez determinadas las Posibilidades para cada Entidad, se procede a combinar dichas posibilidades y generar las combinaciones finales. Estos pasos pueden verse detallados a continuación
#### 2.1 Generación de Posibilidades por Entidad.
  - Una Posibilidad es una posible combinación de ofertas para una Entidad en particular. Una Entidad puede ofertar 1 o más Lotes por lo que hay que determinar todas las combinaciones posibles con esas ofertas. Para hacerlo se tienen en cuenta los [criterios de riesgo y selección](#análisis-de-riesgo-y-criterio-de-selección-de-oferentes). Por ejemplo, una Entidad podría ofertar 3 Lotes dándonos 2&sup3; = 8 posibles combinaciones de Oferta para esa Entidad. Una adjudicándole sólo el primer Lote, otra sólo el segundo, otra sólo el tercero, otra con los dos primeros, etc. Así hasta terminar todas las posibilidades. De esas 8 ofertas tal vez haya alguna que no cumpla con los criterios y queden descartadas de antemano (Para profundizar en las cuentas ir a la sección de [Matematizando un poco las cosas](#matematizando-un-poco-las-cosas)). Este proceso se realiza para todas las Entidades ingresadas sobre todas las Ofertas que hayan hecho. Para ver un ejemplo en concreto ver la seccíon de [Ejemplo](#ejemplo-práctico)

#### 2.2 Generación de Posibilidades con Descuentos por Entidad
  - Una vez finalizada la generación de Posibilidades por Entidad, se procede a generar, de forma análoga, las Posibilidades con Descuentos por Entidad. Como el nombre lo indica, esta generación de Posibilidades se realiza teniendo en cuenta los descuentos. Se realizará el proceso de generación una vez por cada descuento que la Entidad haya ofrecido. La idea detrás de esto es tener todo un conjunto de Posibilidades ya factibles para las empresas, considerando y sin considerar los descuentos, para luego hacer las combinaciones de todas las Posibilidades entre si. 

La generación de Posibilidades con y sin descuento se realizan en un mismo proceso en forma recursiva. 
A continuación se muestra un pseudocódigo utilizado para generar dichas Posibilidades:

```python
#entidades -> Todas las entidades ingresadas
#entidad.descuentos -> referencia a los descuentos de una entidad
#entidad.ofertas -> referencia a las ofertas de una entidad

def calcular_posibilidades():
    for entidad in entidades:
        for descuento in entidad.descuentos:
            generar_posibilidades(new Posibilidad(descuento), entidad.ofertas) #Se instancia una posibilidad por cada descuento. (existe un descuento nulo que se cumple siempre)
        
def generar_posibilidades(posibilidad, ofertas):
    ofertas_usadas = set()
    for oferta in ofertas:
        ofertas_usadas.add(oferta):
        if posibilidad.acepta(oferta): #Devuelve true si la posibilidad acepta esa oferta, es decir, si cumple con los criterios 
            posibilidad.agregar(oferta) #Agrega la oferta a la posibilidad
            if posibilidad.descuento_completo(): #Devuelve true si el descuento propio de la posibilidad ya puede ser aplicado
                posibilidades.append(posibilidad) #Agrega la posibilidad a la lista de posibilidades
            generar_posibilidades(posibilidad, ofertas - ofertas_usadas()) #Llamado recursivo con todas las ofertas menos las usadas
```

#### 2.3 Generación de Combinaciones
  - Una vez alcanzada esta estapa, ya se conocen todas las Posibilidades de Oferta de cada Entidad y si dicha Posibilidad cuenta con un descuento o no. Lo que sige, es tomar todas esas Posibilidades y combinarlas entre si formando la Combinaciones finalmente buscadas. Tanto las Posibilidades como las Combinaciones son combinaciones propiamente dichas. El motivo por el que se llaman distinto, es para poder diferenciar de que tipo de combinación se está hablando. Si se habla de una Posibilidad, se habla de una combinación de Ofertas que una determinada Entidad puede realizar. Y cuando se habla de una Combinación, se hace referencia a una combinación de Posibilidades, es decir, a una combinación de combinaciones (Que es la que finalmente refleja lo que se desea, poder determinar a que Entidad adjudicarle que lote y si correspondería el descuento o no). 
  
Estas Combinaciones se generan de forma muy similar a las Posibilidades. Se realiza con un algoritmo recursivo encargado de generar todos los escenarios posibles. 
A continuación se muestra un pseudocódigo utilizado para generar dichas Combinaciones:

```python
#entidades -> Todas las entidades ingresadas
#entidad.posibilidades -> referencia a las posibilidades de oferta de una entidad
#entidad.ofertas -> referencia a las ofertas de una entidad

def calcular_combinaciones():
    generar_combinaciones(Combinacion(), entidades)

def generar_combinaciones(combinacion, entidades):
    entidades_usadas = set()
    for entidad in entidades:
        entidades_usadas.add(entidad)
        for posibilidad in entidad.posibilidades:
            if combinacion.acepta_posibilidad(posibilidad): #Devuelve true si la combinación acepta esa posibilidad. Solo se acepta una posibilidad si la intersección entre las ofertas contenidas en la combinación y las ofertas contenidas en la posibilidad es nula.
                combinacion.agregar_posibilidad(posibilidad) #Agrega la posibilidad a la combinación
                agregar_combinacion(combinacion) #Agrega la combinación a la lista de combinaciones
                if not combinacion.esta_completa(lotes): #Si la combinacion todavía tiene lotes sin ofertar
                    generar_combinaciones(combinacion, entidades - entidades_usadas) #Llamado recursivo con todas las entidades menos las usadas
```

### 3. Determinación del ganador y muestra de datos
Llegado a la etapa final del proceso, nos encontramos con todas las posibles Combinaciones ya generadas y contamos con la información sobre los descuentos aplicados a cada una. Sólo nos resta determinar la mejor, en otras palabras, determinar las Entidades ganadoras y determinar que Lotes se les adjudicaron a cada una. Esto se lleva a cabo en cuatro mini-pasos más

#### 3.1 Reducción de Combinaciones
  - Como lo que se busca es saber, de todas las posibles Combinaciones, cuál es la ganadora, es necesario primero calcularlas todas. Suena lógico y hasta obvio pero no lo es tanto. El calcular todas implica por ejemplo tener Combinaciones donde solo se le adjudique un Lote a una Entidad, o donde se le adjudique solo ese mismo Lote a otra Entidad, o a otra.. Lo mismo con todos los lotes y todas las Entidades. Y de igual forma para un solo Lote, para dos Lotes, para tres Lotes, para los n Lotes. Entonces nos encontramos con una lista de combinaciones realmente muy grande, estamos hablando de combinaciones de combinaciones en donde los número crecen rápidamente (para más info consultar la sección de [Matematizando un poco las cosas](#matematizando-un-poco-las-cosas)). Para poder hacer los cálculos más rápido es necesario, entonces, reducir la lista de Combinaciones según algún criterio. El criterio que se utiliza es dejar vivas sólo las Combinaciones máximas. Una Combinación es máxima cuando no hay otra Combinación que tenga más Lotes adjudicados que esta. Aplicando este criterio, nos quedaremos con las Combinaciones que tengan la mayor cantidad de Lotes adjudicados descartando todas las demás. Ésto nos reducirá en gran medida la cantidad de Combinaciones y acelerará los cálculos finales.

#### 3.2 Ordenamiento de Combinaciones
  - Cómo el nombre lo indica, se refiere al proceso de aplicarle un orden a la lista de Combinaciones ya reducida. Ésto se realiza en memoria por lo que el paso de reducción es fundamental. El orden será descendente y se tendrá en cuenta el valor final de la Combinación calculada como la suma de todas las ofertas que la continene menos los descuentos aplicados.

#### 3.3 Determinación del Ganador
  - Una vez que la lista se encuentra populada, reducida y ordenada, se determina al ganador simplemente obteniendo el primer elemento de la lista ya que será el de adjudicaciones máximas y menor precio.

#### 3.4 Muestra de Datos
  - Llegamos por fin al último paso en el que se mostrarán los resultados finales de la licitación. Se presentará una pantalla mostrando la Combinación ganadora y otra mostrando todas las Combinaciones (Máximas) generadas. Aquí se puede obtener toda la información requerida en forma prolija e intuitiva. 

Hasta aquí la explicación del funcionamiento del LicitaSoft. En adelante se mencionan diferentes aspectos de interés a quién quiera profundizar un poco más en el funcionamiento del mismo.

## Análisis de Riesgo y Criterio de Selección de Oferentes
Un problema que debe solucionar el LicitaSoft es la generación de todas las posibles Combinaciones de Ofertas y la determinación de la Combinación ganadora. Ahora, el software no solo se programó para eso, sino que también posee cierta inteligencia para determinar el grado de riesgo de las Combinaciones y descartar las de riego más alto. Para eso se definieron criterios de selección que deben cumplir las Entidades participantes. Dichos criterios se detallan a continuación:
  - [x] Para adjudicarle _n_ Lotes a una Entidad, ésta debe contar con al menos _n+1_ contratos concretados anteriormente.
  - [x] Para adjudicarle _n_ Lotes a una Entidad, ésta debe contar con una [experiencia](#) mayor o igual a la [experiencia requerida](#) por los Lotes. 
  - [x] Para adjudicarle _n_ Lotes a una Entidad, ésta debe
    - si es una Empresa, contar con [recursos financieros](#) mayores o iguales a los [recursos financieros requeridos](#) por los lotes.
    - si es una Asociación, contar con [recursos financieros](#) mayores o iguales a los [recursos financieros requeridos](#) por los lotes. Además cada Socio debe contar con, al menos, el 25% de los [recursos financieros requeridos](#) por los Lotes. Y por lo menos un socio debe contar con, al menos, el 40% de los [recursos financieros requeridos](#) por los Lotes.
  - [x] Para adjudicarle _n_ Lotes a una Entidad, ésta debe
    - si es una Empresa, contar con una [facturación media anual](#) mayor o igual a la [facturación media anual requerida](#) por los lotes.
    - si es una Asociación, contar con una [facturación media anual](#) mayor o igual a la [facturación media anual requerida](#) por los lotes. Además, cada Socio debe contar con, al menos, el 20% de la [facturación media anual requerida](#) por los Lotes, pudiendo sólo un Socio no cumplir con este criterio pero debiendo cumplir con, al menos, el 15% de la misma. Y por lo menos un Socio debe contar con, al menos, el 40% de la [facturación media anual](#) por los Lotes.
  
#### Atributos de una Entidad
##### Experiencia
La experiencia de una Enitdad-Empresa se calcula como la suma del valor de los mayores _n+1_ contratos donde _n_ es la cantidad de Lotes adjudicados. 
La experiencia de una Entidad-Asociación se calcula como la suma del valor de los mayores _n+1_ contratos de todos los Socios que la componen, donde _n_ es la cantidad de Lotes adjudicados.

##### Facturación Media Anual
La facturación media anual de una Entidad-Empresa es un dato que se ingresa en la primera etapa del proceso
La facturación media anual de una Entidad-Asociación se calcula como la suma de la facturación media anual de todos los Socios que la componen.

##### Recursos Financieros 
Los recursos financieros de una Entidad-Empresa es un dato que se ingresa en la primera etapa del proceso
Los recursos financieros de una Entidad-Asociación se calculan como la suma de los recursos financieros de todos los Socios que la componen.

#### Atributos de una Posibilidad
##### Experiencia Requerida
La experiencia requerida se calcula como la suma de la experiencia requerida de los _n_ Lotes adjudicados.

##### Facturación Media Anual Requerida
La facturación media anual requerida se calcula como la suma de la facturación media anual requerida de los _n_ Lotes adjudicados.

##### Recursos Financieros Requeridos
Los recursos financieros requeridos se calcula como la suma de los recursos financieros requeridos de los _n_ Lotes adjudicados.

## Ejemplo Práctico

## Matematizando un poco las cosas
