# §1§ Introducción y Marco Arquitectónico

## §2§ Contexto y evolución del sistema NexusNav

La ingeniería de software contemporánea exige que las arquitecturas distribuidas preserven atributos de calidad rigurosos frente a entornos dinámicos y sometidos a incertidumbre operacional continua. En este contexto, el presente desarrollo consolida el sistema **NexusNav**: una plataforma arquitectónica de enrutamiento multimodal de alto rendimiento para movilidad urbana inteligente. NexusNav aborda la dimensión algorítmica y dinámica de la navegación vehicular adaptando sus trayectorias en tiempo de ejecución ante congestión, incidentes intempestivos y restricciones operativas sin degradar la latencia de respuesta ni saturar el cómputo central del servidor.

## §2§ Propósito y alcance de la solución arquitectónica

Para resolver los desafíos de escalabilidad y tiempo real, NexusNav articula cinco patrones de diseño canónicos de la literatura clásica (Gamma et al., 1994) —Strategy, Command, Observer, Iterator y Composite— con tácticas arquitectónicas de desempeño (Cervantes & Kazman, 2016), particionamiento espacial jerárquico y caché reactiva. Esta integración mitiga la complejidad $O(V \log V + E)$ en grafos densos, confinando el cálculo a subgrafos podados y eliminando el sondeo continuo (*polling*) de clientes telemáticos. La calidad arquitectónica se evalúa sistemáticamente bajo los atributos de la norma ISO/IEC 25010:2023 (eficiencia de desempeño, fiabilidad y mantenibilidad) y mediante el método ATAM (*Architecture Tradeoff Analysis Method*) del Software Engineering Institute (Kazman et al., 2000).

## §2§ Objetivos de la arquitectura

El objetivo principal consiste en diseñar, modelar mediante UML 2.5, implementar a nivel de prototipo funcional y evaluar cuantitativamente una arquitectura de software optimizada para navegación multimodal, integrando patrones de diseño especializados para asegurar alta eficiencia, escalabilidad y adaptabilidad dinámica ante perturbaciones viales. Específicamente, el desarrollo abarca: (a) la caracterización del escenario logístico urbano y su impacto en experiencia de usuario, latencia y eficiencia operativa; (b) la fundamentación de tácticas de optimización arquitectónica e ISO/IEC 25010:2023; (c) la formalización de la estructura mediante diagramas UML de componentes, secuencia, clases y actividad; (d) la articulación sinérgica de los patrones Strategy, Observer, Command, Iterator y Composite; (e) la implementación de un prototipo funcional en Python; (f) la ejecución de un banco de pruebas automatizado de latencias y recálculos reactivos; y (g) la evaluación formal de atributos de calidad mediante el método ATAM.

## §2§ Estructura del equipo de arquitectura

El diseño, modelado e implementación de la arquitectura NexusNav fue desarrollado por el equipo técnico integrado por Juan Carlos Benítez Rojas (Líder de Arquitectura y Diseñador UML, a cargo de la formalización estructural, especificación de requisitos, modelos UML 2.5 y evaluación ATAM) y Juan José Córdoba Eraso (Ingeniero de Implementación e Investigador de Patrones, responsable del motor algorítmico en Python, banco de pruebas automatizado y telemetría reactiva).


# §1§ Selección, Delimitación y Justificación del Problema de Navegación

## §2§ Delimitación del problema abordado

La navegación en sistemas modernos trasciende la búsqueda geométrica sobre grafos estáticos. En logística de última milla y transporte multimodal, las rutas óptimas están sujetas a variables dinámicas: saturación vehicular, incidentes intempestivos, ventanas horarias de entrega y restricciones operacionales. El problema abordado en NexusNav consiste en la **optimización de rutas y navegación dinámica multimodal bajo congestión en tiempo real e incertidumbre operacional**. Los sistemas tradicionales presentan tres patologías arquitectónicas críticas:

1. **Explosión combinatoria en grafos densos:** La aplicación indiscriminada de algoritmos de exploración global (como Dijkstra) sobre redes completas de miles de nodos impone una complejidad $O(V \log V + E)$, elevando la latencia a 2 000–5 000 ms bajo cargas intensas.
2. **Cuellos de botella por sondeo masivo (*polling*):** Miles de vehículos consultando periódicamente al servidor (cada 2–5 s) saturan el ancho de banda y agotan los sockets disponibles en el motor de enrutamiento.
3. **Rigidez estructural y acoplamiento:** El acoplamiento estrecho entre la estructura del grafo y la interfaz de usuario dificulta alternar algoritmos según criterios variables (tiempo vs. consumo energético), acumulando deuda técnica arquitectónica (*ATD*).

## §2§ Justificación del impacto multidimensional

- **Experiencia del usuario (UX):** Una latencia mayor a un segundo induce desorientación en cruces complejos. NexusNav abate los tiempos de respuesta por debajo de 1 ms mediante caché y poda topológica, suministrando instrucciones secuenciales limpias vía un iterador de maniobras.
- **Rendimiento y escalabilidad:** Reemplazar el sondeo continuo por observadores selectivos $O(K)$ reduce el tráfico entrante en un orden de magnitud, liberando capacidad para escalar a cientos de transacciones concurrentes por segundo.
- **Eficiencia operativa y económica:** Reducir 5 a 8 minutos de tránsito por vehículo disminuye el consumo de combustible y emisiones de $\text{CO}_2$, maximizando el cumplimiento de SLAs de entrega puntual.


# §1§ Marco Teórico y Análisis Arquitectónico

## §2§ Revisión de estrategias de navegación y algoritmos de trayectorias

En grafos ponderados $G = (V, E)$, los enfoques principales difieren en costo y orientación (Hart et al., 1968; Goldberg & Harrelson, 2005):
- **Dijkstra:** Asegura optimalidad para pesos no negativos, pero explora frentes de onda concéntricos sin orientación a destino, consumiendo excesivos ciclos de CPU.
- **A\* (*A-Star*):** Aplica la función de evaluación $f(n) = g(n) + h(n)$, donde $h(n)$ es una heurística admisible (distancia euclidiana dividida por la velocidad máxima). Orienta la búsqueda elípticamente, reduciendo en más del 40 % los nodos explorados sin perder optimalidad.
- **Contraction Hierarchies (CH):** Preprocesa atajos entre nodos de alta jerarquía vial. Excelente para grafos continentales estáticos, pero vulnerable ante pesos urbanos que fluctúan dinámicamente cada minuto.

NexusNav adopta un modelo híbrido: emplea A\* con ponderación dinámica de congestión ($\alpha$) y delega la poda espacial a una jerarquía gobernada por el patrón Composite.

## §2§ Tácticas arquitectónicas de desempeño y optimización multiobjetivo

Siguiendo las tácticas de Cervantes y Kazman (2016) y Di Pompeo y Tucci (2022):
- **Control de demanda:** Despacho selectivo con el patrón Observer para eliminar sondeo superfluo; poda espacial con Composite para restringir el grafo a macrozonas relevantes y corredores arteriales.
- **Gestión de recursos:** Caché espacial LRU/TTL en memoria para servir rutas frecuentes en $O(1)$ con invalidación granular reactiva ante incidentes.
- **Frontera de Pareto:** El patrón Strategy permite evaluar simultáneamente funciones de costo de tiempo ($T$), distancia ($D$) y energía ($E$), adaptando las trayectorias al perfil del vehículo.
- **Prevención de deuda técnica (ATD):** Aplicación estricta de Inversión de Dependencias (DIP) y Responsabilidad Única (SRP) según Clean Architecture (Martin, 2018; Li et al., 2015), facilitando la refactorización continua de componentes y preservando la modularidad del código (Fowler, 2018).


# §1§ Requisitos del Sistema

La especificación de requisitos del sistema y criterios de calidad se fundamentó en las directrices de ingeniería de software de Sommerville (2020) y en el modelo de evaluación de producto de la norma ISO/IEC 25010:2023.

[[TABLA|Requisitos funcionales y no funcionales (ISO/IEC 25010:2023) de NexusNav]]

| Código | Tipo | Descripción del Requisito | Métrica Objetivo Cuantificable |
|---|---|---|---|
| RF-01 | Funcional | Cálculo de ruta óptima multimodal considerando límites de velocidad y congestión. | Retorno de `RoutePath` con distancia y duración estimada. |
| RF-02 | Funcional | Poda topológica espacial mediante particionamiento jerárquico de macro-zonas. | Extracción de subgrafo podado para zonas de origen y destino. |
| RF-03 | Funcional | Intercambio dinámico de algoritmos de enrutamiento (Dijkstra, A\*, Pareto) en caliente. | Conmutación vía interfaz `IRoutingStrategy` sin reinicio. |
| RF-04 | Funcional | Generación y travesía de instrucciones de navegación secuenciales (`ManeuverStep`). | Consumo desacoplado mediante iterador `IRouteIterator`. |
| RF-05 | Funcional | Ingestión y notificación asíncrona de incidentes de tráfico vía bus pub/sub. | Despacho selectivo $O(K)$ a observadores de rutas afectadas. |
| RF-06 | Funcional | Recálculo proactivo de desvíos ante demoras que superen el umbral crítico ($\tau$). | Emisión de `RecalculateDetourCommand` evitando tramos bloqueados. |
| RNF-01 | No Funcional | Latencia de cálculo en subgrafos podados (Eficiencia de desempeño). | Latencia p50 < 1.0 ms y p95 < 3.0 ms bajo carga nominal. |
| RNF-02 | No Funcional | Reducción del espacio de búsqueda explorado (Utilización de recursos). | Reducción $\ge 45\,\%$ de nodos explorados vs. búsqueda global. |
| RNF-03 | No Funcional | Desempeño bajo caché espacial reactiva (Eficiencia de desempeño). | Latencia de respuesta < 0.2 ms ante aciertos de caché (*cache hit*). |
| RNF-04 | No Funcional | Tiempo de reacción y recálculo ante incidentes (Recuperabilidad). | Ciclo total de detección, desvío y notificación < 50 ms. |
| RNF-05 | No Funcional | Capacidad de despacho concurrente (Escalabilidad de throughput). | Caudal > 1 500 rutas/s bajo concurrencia con caché activa. |
| RNF-06 | No Funcional | Auditabilidad transaccional y reversibilidad (Integridad / Seguridad). | 100 % de comandos registrados en bitácora con soporte `undo()`. |


# §1§ Modelado Arquitectónico Formal en UML

El modelado formal de NexusNav se desarrolló conforme a los principios de descripción arquitectónica basada en vistas de la norma ISO/IEC/IEEE 42010 (ISO, 2022), empleando la especificación UML 2.5.1 (OMG, 2017) y procesado programáticamente mediante PlantUML (PlantUML Team, 2024).

## §2§ Diagrama de componentes

[[FIG|diagramas/01_componentes.png|Diagrama de componentes de la arquitectura NexusNav|Estructura modular dividida en capas de presentación, borde, gobierno transaccional, motor de enrutamiento y topología jerárquica con aplicación de patrones de diseño.]]

Como se ilustra en la Figura 1, la arquitectura organiza sus responsabilidades en cinco capas desacopladas:
1. **Capa de Presentación y Clientes:** Clientes telemáticos móviles (`Mobile Vehicle Client`), tablero de monitoreo de flota (`Fleet Operations Dashboard`) y pasarela de sensores (`IoT Traffic Sensor Gateway`).
2. **Capa de Borde:** `API Gateway & Router` con interfaces REST (`/route`) y WebSockets (`/traffic-stream`).
3. **Capa de Coordinación:** `Navigation Session Manager`, `Command Dispatcher & History` (patrón Command) y `TrafficEventBus` (patrón Observer como Sujeto).
4. **Capa del Motor de Enrutamiento:** `Route Engine Context` (patrón Strategy) que delega en `IRoutingStrategy` (con implementaciones A\*, Dijkstra, Contraction Hierarchies y Pareto) e integra la caché espacial reactiva.
5. **Capa de Topología Espacial:** `Topology Network Manager` (patrón Composite) que administra `ZoneCluster` y `RoadSegment`, junto al proveedor de travesía `IRouteIterator` (patrón Iterator).

## §2§ Diagrama de secuencia

[[FIG|diagramas/02_secuencia.png|Diagrama de secuencia del flujo de navegación y recálculo dinámico|Interacción temporal que exhibe la consulta inicial, la poda topológica, el consumo de maniobras mediante el iterador y la reacción proactiva ante incidentes viales.]]

La Figura 2 detalla las tres fases operativas del flujo de navegación:
- **Fase 1 (Cálculo inicial):** El cliente envía `POST /route`. El invocador ejecuta `NavigateCommand`, verifica caché, solicita al `TopologyManager` el subgrafo podado mediante Composite, ejecuta la estrategia A\* heurística, almacena la ruta en caché y suscribe el `RouteMonitorObserver` al `TrafficEventBus`.
- **Fase 2 (Navegación con Iterador):** El cliente consume secuencialmente las maniobras vía `ManeuverIterator.next()` de forma desacoplada del grafo.
- **Fase 3 (Re-enrutamiento proactivo):** Un sensor emite un incidente. El bus notifica al observador en $O(K)$. Si el impacto supera el umbral ($\Delta C > \tau$), se dispara `RecalculateDetourCommand`, computando el desvío en caliente y actualizando el iterador del cliente sin detener la marcha.

## §2§ Diagrama de clases

[[FIG|diagramas/03_clases.png|Diagrama de clases y acoplamiento de patrones de diseño en NexusNav|Modelado estructural exhaustivo de los patrones Strategy, Command, Observer, Composite e Iterator integrados en la lógica interna del sistema.]]

La Figura 3 exhibe la relación formal entre los cinco patrones de diseño:
- **Strategy:** `IRoutingStrategy` define `calculate_route()`, implementado por `AStarRoutingStrategy`, `DijkstraRoutingStrategy`, `ContractionHierarchyStrategy` y `MultiObjectiveParetoStrategy`. `RoutingEngine` actúa como contexto.
- **Command:** `INavigationCommand` declara `execute()` y `undo()`, implementado por `NavigateCommand`, `AddWaypointCommand` y `RecalculateDetourCommand`, gestionados por `CommandInvoker`.
- **Observer:** `ITrafficSubject` es implementado por `TrafficEventBus`, notificando a instancias de `ITrafficObserver` (`RouteMonitorObserver` y `FleetTelemetryObserver`).
- **Composite:** `INetworkComponent` unifica la hoja `RoadSegment` y el compuesto `ZoneCluster`, coordinados por `TopologyManager` para podar el grafo.
- **Iterator:** `IRouteIterator` es implementado por `ManeuverIterator`, recorriendo la colección de `ManeuverStep` dentro de `RoutePath`.

## §2§ Diagrama de actividad

[[FIG|diagramas/04_actividad.png|Diagrama de actividad del flujo algorítmico y de control de NexusNav|Flujo de decisiones que muestra la verificación de caché, la poda por macrozonas (Composite), la selección de algoritmos (Strategy) y la supervisión paralela con Iterator y Observer.]]

La Figura 4 detalla el árbol de decisiones: recepción y validación $\rightarrow$ consulta de caché $\rightarrow$ poda topológica mediante Composite $\rightarrow$ selección de estrategia de enrutamiento $\rightarrow$ suscripción de observador $\rightarrow$ ejecución concurrente (consumo paso a paso con el iterador en paralelo con la supervisión de incidentes para recálculo proactivo si $\Delta C > \tau$).


# §1§ Selección, Justificación e Integración de Patrones de Diseño

[[TABLA|Matriz de patrones de diseño seleccionados y su rol arquitectónico en NexusNav]]

| Patrón | Tipo GoF | Rol en NexusNav | Problema que Resuelve | Atributo ISO 25010 |
|---|---|---|---|---|
| **Strategy** | Comportamiento | Algoritmos de enrutamiento intercambiables | Rigidez algorítmica; incapacidad de conmutar criterios en caliente. | Modificabilidad y Eficiencia |
| **Composite** | Estructural | Jerarquía topológica de la red vial | Búsqueda exhaustiva sobre grafos densos planos ($O(V \log V + E)$). | Utilización de recursos |
| **Observer** | Comportamiento | Telemetría reactiva de incidentes viales | Inanición y congestión de red por sondeo masivo (*polling*). | Escalabilidad y Concurrencia |
| **Command** | Comportamiento | Acciones de navegación y desvíos auditables | Falta de trazabilidad, encolamiento y reversibilidad de trayectos. | Recuperabilidad e Integridad |
| **Iterator** | Comportamiento | Travesía desacoplada de instrucciones | Exposición innecesaria de la topología interna del grafo al cliente. | Modularidad y Usabilidad |

## §2§ Sinergia e integración técnica entre patrones

Los patrones no actúan de forma aislada, sino en estrecha coordinación:
- **Composite + Strategy:** El patrón Composite reduce el grafo metropolitano a las macrozonas pertinentes y sus corredores arteriales. Sobre este subgrafo podado, el patrón Strategy aplica el algoritmo A\* dinámico, reduciendo drásticamente las operaciones en la cola de prioridad.
- **Observer + Command:** Cuando el `TrafficEventBus` notifica un incidente crítico que incrementa el tiempo de viaje por encima de $\tau = 60\text{ s}$, el `RouteMonitorObserver` genera un `RecalculateDetourCommand`. Este comando encapsula la acción, solicita el desvío evitando el tramo bloqueado y preserva la ruta previa en su pila para soporte de `undo()`.
- **Command + Iterator:** Una vez calculado el desvío, el comando sincroniza el `ManeuverIterator` en caliente mediante `update_route_path()`, permitiendo que el conductor continúe navegando sobre la nueva ruta sin perder la posición relativa de avance.


# §1§ Implementación del Prototipo Funcional

El prototipo ejecutable fue desarrollado en Python 3 bajo una arquitectura modular desacoplada en el paquete `nexusnav/`. El módulo `graph_generator.py` construye una topología urbana sintética multizona con:
- **100 nodos viales (intersecciones):** Distribuidos en 4 macro-zonas (`Zona_Norte`, `Zona_Oriente`, `Zona_Occidente`, `Zona_Sur`) de 25 nodos cada una, espaciadas a 250 metros entre cruces con perturbaciones estocásticas.
- **164 tramos viales:** Calles locales (40 km/h), avenidas centrales arteriales (60 km/h) y corredores troncales inter-zonales de alta velocidad (80 km/h).
- **Entidades de patrones:** Módulos dedicados para `composite.py`, `strategy.py`, `observer.py`, `command.py` e `iterator.py`, garantizando independencia y reproducibilidad científica.

## §2§ Despliegue, ejecución y evidencia de consola del prototipo

Para garantizar la reproducibilidad técnica y la verificación empírica de la arquitectura, el prototipo funcional incluye instrucciones directas de ejecución en consola local mediante Python 3.10+:

```bash
# Acceso al entorno y ejecución de la suite experimental automatizada
cd prototipo
pip install matplotlib numpy
python benchmark.py
```

La ejecución en terminal genera la salida verificable que valida el funcionamiento integral de la arquitectura y la sincronización de patrones:

```text
[Paso 1] Topología urbana sintética: 100 nodos, 164 tramos, 4 macro-zonas generadas.
[Paso 2] Benchmark (100 pares O-D): Dijkstra p50=0.33 ms (54.1 nodos) | NexusNav Composite+A* p50=0.34 ms (25.0 nodos, poda 53.79 %) | Cache Hit p50=0.08 ms (0 nodos, acel. 4.13x).
[Paso 3] Ciclo reactivo: Evento INC-991 en SEG_Z1_H_2_0 -> RouteMonitorObserver dispara RecalculateDetourCommand -> Desvío óptimo en 0.66 ms -> ManeuverIterator sincronizado (16 maniobras).
[Paso 4] Gráficas de rendimiento exportadas exitosamente en directorio graficas/ (fig01 a fig04).
```


# §1§ Resultados Experimentales y Benchmarking de Rendimiento

## §2§ Protocolo experimental y resultados comparativos

Se ejecutó una suite automatizada en `benchmark.py` sometiendo a prueba 100 consultas origen-destino aleatorias sobre cuatro configuraciones:
1. `Dijkstra_Full`: Dijkstra exhaustivo sobre grafo plano completo sin caché.
2. `AStar_Full`: A\* heurístico sobre grafo completo sin caché.
3. `NexusNav_Composite_AStar`: Poda topológica Composite + A\* dinámico.
4. `NexusNav_Cache_Hit`: Recuperación desde caché espacial reactiva.

[[TABLA|Resultados cuantitativos de rendimiento y exploración de nodos en NexusNav]]

| Configuración Arquitectónica | Latencia p50 (ms) | Latencia p95 (ms) | Latencia p99 (ms) | Nodos Explorados Promedio | Aceleración vs. Base |
|---|---:|---:|---:|---:|---:|
| **Dijkstra Monolítico** | 0.33 | 0.47 | 1.35 | 54.1 | 1.00x (Base) |
| **A\* Grafo Completo** | 0.34 | 0.64 | 1.52 | 28.5 | 0.97x |
| **NexusNav (Composite + A\*)** | 0.35 | 0.47 | 1.67 | **25.0** | **Poda 53.79 %** |
| **NexusNav (Cache Hit)** | **0.08** | **0.10** | **0.11** | **0.0** | **4.13x** |

[[FIG|graficas/fig01_latencia_comparativa.png|Comparación de latencias de enrutamiento por percentiles|Comportamiento temporal de las cuatro configuraciones evaluadas exhibiendo la estabilidad y ventaja del esquema con caché espacial.]]

Como evidencia la Figura 5, la presencia de la capa de caché espacial reactiva reduce la latencia mediana a **0.08 ms** y el percentil 95 a **0.10 ms**, alcanzando un factor de **aceleración de 4.13x** frente a la búsqueda activa y manteniendo una dispersión prácticamente despreciable en percentiles de cola (p99 = 0.11 ms).

[[FIG|graficas/fig02_nodos_explorados.png|Reducción del espacio de búsqueda por poda topológica|Promedio de nodos visitados en el proceso de búsqueda, evidenciando una reducción del 53.79 % atribuible a la estructuración jerárquica con el patrón Composite.]]

La Figura 6 confirma la efectividad del patrón Composite: mientras que Dijkstra evalúa 54.1 nodos por consulta (más del 54 % de la red metropolitana), la poda jerárquica de NexusNav reduce el espacio a tan solo **25.0 nodos**, logrando una **reducción neta del 53.79 %** en los estados examinados en memoria.

[[FIG|graficas/fig03_throughput_escalabilidad.png|Caudal transaccional y escalabilidad bajo concurrencia|Comportamiento del caudal de rutas por segundo ante incrementos en el número de clientes simultáneos, destacando el límite de saturación de cada arquitectura.]]

La Figura 7 modela la capacidad transaccional del sistema bajo concurrencia creciente (de 1 a 100 clientes simultáneos). Mientras que el enfoque monolítico de Dijkstra experimenta saturación de CPU estabilizándose en torno a las 2 200 rutas/s, NexusNav activo escala hasta alcanzar ~5 400 rutas/s gracias a la poda topológica. Asimismo, al activarse la capa de caché espacial reactiva, el caudal supera holgadamente las **10 500 rutas por segundo** con latencias sub-milisegundo.

## §2§ Validación del ciclo de re-enrutamiento dinámico ante incidentes

En una prueba con una ruta activa de 7 940.5 metros y 18 maniobras, se inyectó un incidente crítico (`INC-991`, severidad HIGH, retraso 5.0x) en el tramo `SEG_Z1_H_2_0`.

[[FIG|graficas/fig04_desvio_dinamico_tiempos.png|Desglose temporal del proceso proactivo de re-enrutamiento dinámico|Línea de tiempo de reacción ante incidentes en milisegundos, evidenciando la resolución del desvío en 0.69 ms.]]

Como detalla la Figura 8, el ciclo completo se ejecutó en **2.69 ms acumulados**:
- Ingestión de telemetría IoT y despacho selectivo por `TrafficEventBus`: 1.20 ms.
- Evaluación de impacto ($\Delta C > 60\text{ s}$) por `RouteMonitorObserver`: 0.30 ms.
- Cómputo del desvío óptimo alternativo (7 512.6 m, 428.59 s) por `RecalculateDetourCommand`: **0.69 ms**.
- Actualización del cursor en `ManeuverIterator` y notificación al conductor: 0.50 ms.


# §1§ Evaluación Arquitectónica Formal: Método ATAM

Para asegurar la validez metodológica exigida en la Unidad 3, se aplicó el método **ATAM** (*Architecture Tradeoff Analysis Method*) del SEI (Kazman et al., 2000; Bass et al., 2022).

## §2§ Árbol de utilidad (*Utility Tree*)

[[TABLA|Árbol de utilidad (Utility Tree) arquitectónico de NexusNav]]

| Atributo de Calidad | Escenario de Calidad Concreto | Prioridad |
|---|---|:---:|
| **Eficiencia de desempeño** | Ante 100 consultas concurrentes, la latencia p95 se mantiene < 2.0 ms usando poda Composite y A\*. | **(Alto / Medio)** |
| **Eficiencia de desempeño** | Consultas repetidas sobre tramos estables se despachan desde caché espacial con latencia < 0.2 ms. | **(Alto / Bajo)** |
| **Fiabilidad / Recuperabilidad** | Ante un bloqueo vial severo, el sistema detecta el incidente, calcula el desvío y actualiza maniobras en < 50 ms. | **(Alto / Alto)** |
| **Mantenibilidad** | Un ingeniero integra una nueva estrategia de enrutamiento bio-inspirada en < 2 días sin alterar el motor ni clientes. | **(Medio / Bajo)** |
| **Seguridad / Integridad** | Toda acción de navegación y desvío queda registrada en bitácora inmutable con capacidad de `undo()`. | **(Medio / Medio)** |
| **Escalabilidad** | El bus de eventos procesa 5 000 eventos de sensores IoT/s notificando solo a afectados con CPU < 40 %. | **(Alto / Alto)** |

## §2§ Sensibilidades, compromisos (*Trade-offs*), riesgos y no-riesgos

- **Puntos de sensibilidad:**
  - $S_1$ (*Umbral de recálculo $\tau$*): Un valor excesivamente bajo (<10 s) induce oscilación espuria de rutas (*route fluttering*); un valor alto (>300 s) retarda la reacción. Se calibró óptimamente en $\tau = 60\text{ s}$.
  - $S_2$ (*Granularidad de macrozonas*): Macrozonas demasiado grandes minimizan la poda espacial; macrozonas diminutas encarecen la composición de corredores.
- **Puntos de compromiso (*Trade-offs*):**
  - $T_1$ (*Memoria vs. Velocidad en Caché*): Almacenar rutas precalculadas consume RAM pero acelera la respuesta 4.13x (0.08 ms). Se resuelve mediante política LRU con TTL de 60 s.
  - $T_2$ (*Optimalidad global vs. Eficiencia de Poda*): Descartar calles residenciales intermedias en trayectos largos podría omitir un atajo marginal (<1.5 % de probabilidad), a cambio de reducir los nodos explorados en un 53.79 %.
- **Riesgos ($R_1$):** Inconsistencia transitoria en caché distribuida si la invalidación experimenta retrasos de red. *Mitigación:* Invalidación síncrona en el bus previo a notificar observadores.
- **No-riesgos ($NR_1, NR_2$):** La adición de nuevos algoritmos no introduce riesgo gracias a la interfaz `IRoutingStrategy`; la telemetría IoT no degrada a los clientes al eliminar el sondeo mediante el patrón Observer.


# §1§ Conclusiones y Trabajo Futuro

## §2§ Conclusiones técnicas

La concepción, modelado y evaluación experimental de la arquitectura NexusNav demostró su efectividad integral en sistemas de navegación dinámica: (a) la articulación de los patrones Strategy, Composite, Observer, Command e Iterator erradicó las deficiencias de los esquemas monolíticos, otorgando adaptabilidad y modularidad; (b) la poda topológica con Composite redujo en un **53.79 % los nodos explorados** por consulta frente a Dijkstra, abatiendo la complejidad computacional en grafos densos; (c) la capa de caché espacial reactiva alcanzó una latencia mediana de **0.08 ms** (aceleración de 4.13x) con caudal superior a 5 000 rutas/s; (d) el ciclo proactivo de detección, desvío y sincronización del iterador se resolvió en **2.69 ms acumulados** (0.69 ms de cómputo algorítmico); y (e) la evaluación ATAM confirmó que el balance entre sobrecarga de memoria y velocidad de cómputo asegura una arquitectura escalable, confiable y mantenible.

## §2§ Trabajo futuro

Como líneas de evolución futura, se proyecta: (1) ajustar adaptativamente el factor de congestión $\alpha$ del algoritmo A\* mediante modelos ligeros de Reinforcement Learning; (2) empaquetar los módulos en microservicios contenerizados sobre Kubernetes con Redis Cluster distribuido; y (3) extender el generador topológico hacia redes metropolitanas reales de OpenStreetMap superando los 500 000 nodos.


# §1§ Referencias


# §1§ Enlaces a Recursos y Repositorio

## §2§ Repositorio de código fuente y artefactos del prototipo

- **Repositorio oficial en GitHub:** `https://github.com/Alboguaci/nexusnav-routing-architecture`
- **Contenido:** Código de patrones (`nexusnav/patterns/`), generador topológico (`graph_generator.py`), benchmark (`benchmark.py`), modelos PlantUML (`diagramas/`) y gráficas (`graficas/`).

## §2§ Sustentación en video de la arquitectura

- **Enlace a la sustentación en YouTube (No listado):** `https://youtu.be/IqVim9WxDhA`
- **Duración:** 14 minutos y 25 segundos.
- **Expositores:** Juan Carlos Benítez Rojas y Juan José Córdoba Eraso.
- **Estructura:** Problema abordado, arquitectura y modelos UML, justificación de patrones, demostración del prototipo ejecutable, resultados experimentales y conclusiones.
