# NexusNav: Dynamic Multimodal Routing & Navigation Architecture
### *Arquitectura de Software para Enrutamiento Dinámico de Alto Rendimiento con Patrones GoF, Poda Topológica y Telemetría Reactiva*

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Architecture](https://img.shields.io/badge/Architecture-Clean%20%7C%20UML%202.5-brightgreen.svg)]()
[![Evaluation](https://img.shields.io/badge/Evaluation-ATAM%20%7C%20ISO%2025010-orange.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

NexusNav es una solución arquitectónica de alto rendimiento diseñada para la navegación inteligente y el enrutamiento multimodal dinámico en entornos urbanos y logísticos de alta densidad sometidos a congestión vehicular en tiempo real.

El sistema resuelve la complejidad combinatoria $O(V \log V + E)$ y elimina la sobrecarga de red por sondeo masivo (*polling*) mediante la integración de cinco patrones de diseño de software (Strategy, Composite, Observer, Command e Iterator), combinados con particionamiento espacial jerárquico y una capa de caché reactiva en memoria.

---

## 👥 Equipo de Arquitectura y Desarrollo

- **Juan Carlos Benítez Rojas** — *Líder de Proyecto, Modelado y Diseño de Arquitectura de Software*
- **Juan José Córdoba Eraso** — *Desarrollador del Motor Algorítmico e Investigador de Rendimiento*

---

## 🧭 Desafíos Arquitectónicos Abordados

1. **Explosión combinatoria en grafos densos:** La búsqueda global tradicional (Dijkstra) sobre redes de miles de nodos degrada la latencia bajo cargas concurrentes. NexusNav confina la búsqueda a subgrafos pertinentes mediante poda topológica.
2. **Cuellos de botella por sondeo masivo (*polling*):** Clientes telemáticos consultando periódicamente saturan el ancho de banda. NexusNav implementa despacho reactivo pub/sub selectivo $O(K)$.
3. **Rigidez algorítmica y deuda técnica:** El acoplamiento estrecho entre topología y algoritmos dificulta alternar criterios (tiempo vs. distancia vs. energía). NexusNav aplica Inversión de Dependencias (DIP) y Responsabilidad Única (SRP).

---

## 🧩 Patrones de Diseño Implementados

| Patrón | Tipo GoF | Rol en NexusNav | Problema que Resuelve | Atributo ISO 25010 |
|---|---|---|---|---|
| **Strategy** | Comportamiento | Algoritmos de enrutamiento intercambiables (A*, Dijkstra, Pareto) | Rigidez algorítmica; incapacidad de conmutar criterios en caliente. | Modificabilidad y Eficiencia |
| **Composite** | Estructural | Jerarquía topológica urbana en macro-zonas (`ZoneCluster`) | Búsqueda exhaustiva sobre grafos densos planos ($O(V \log V + E)$). | Utilización de recursos |
| **Observer** | Comportamiento | Telemetría reactiva de incidentes viales (`TrafficEventBus`) | Inanición y congestión de red por sondeo masivo (*polling*). | Escalabilidad y Concurrencia |
| **Command** | Comportamiento | Acciones de navegación y desvíos auditables con reversión (`undo`) | Falta de trazabilidad, encolamiento y reversibilidad de trayectos. | Recuperabilidad e Integridad |
| **Iterator** | Comportamiento | Travesía desacoplada de instrucciones secuenciales (`ManeuverStep`) | Exposición innecesaria de la topología interna del grafo al cliente. | Modularidad y Usabilidad |

---

## 📊 Resultados del Benchmarking Experimental

Sometido a un banco de pruebas de 100 consultas origen-destino sobre una red sintética de 100 intersecciones y 164 tramos viales:

| Configuración Arquitectónica | Latencia p50 (ms) | Latencia p95 (ms) | Latencia p99 (ms) | Nodos Explorados | Factor Aceleración |
|---|---:|---:|---:|---:|---:|
| **Dijkstra Monolítico** | 0.33 | 0.47 | 1.35 | 54.1 | 1.00x (Base) |
| **A\* Grafo Completo** | 0.34 | 0.64 | 1.52 | 28.5 | 0.97x |
| **NexusNav (Composite + A\*)** | 0.35 | 0.47 | 1.67 | **25.0** | **Poda neta 53.79 %** |
| **NexusNav (Cache Hit)** | **0.08** | **0.10** | **0.11** | **0.0** | **4.13x** |

- **Re-enrutamiento proactivo ante incidentes:** Detección de incidente vial y cómputo de desvío alternativo resuelto en **0.66 ms** (2.69 ms acumulados incluyendo notificación selectiva y sincronización en caliente del iterador).
- **Capacidad de despacho concurrente:** Sostiene hasta **5 400 rutas/s** bajo cómputo activo (Composite + A*) y supera holgadamente las **10 500 rutas/s** con la capa de caché reactiva activa (frente a la saturación temprana de Dijkstra en ~2 200 rutas/s).

---

## 🏛️ Evaluación Arquitectónica Formal: Método ATAM

La arquitectura fue evaluada mediante el método **ATAM** (*Architecture Tradeoff Analysis Method*) del SEI:
- **Árbol de utilidad (*Utility Tree*):** Priorización rigurosa de latencia (<2.0 ms en p95), recuperabilidad ante bloqueos (<50 ms) y throughput concurrente.
- **Puntos de sensibilidad:** Umbral de recálculo dinámico ($\tau = 60\text{ s}$) y granularidad de macro-zonas en el Composite.
- **Puntos de compromiso (*Trade-offs*):** Sobrecarga en memoria RAM de la caché espacial vs. aceleración 4.13x; descarte de calles capilares en viajes largos vs. reducción de 53.79 % en nodos explorados.
- **Riesgos y no-riesgos:** Mitigación de consistencia eventual en invalidación de caché; extensibilidad algorítmica garantizada por Inversión de Dependencias (DIP).

---

## 📁 Estructura del Repositorio

```text
nexusnav-routing-architecture/
├── diagramas/
│   ├── 01_componentes.puml (.png / .svg)
│   ├── 02_secuencia.puml (.png / .svg)
│   ├── 03_clases.puml (.png / .svg)
│   ├── 04_actividad.puml (.png / .svg)
│   └── render_diagrams.py
├── graficas/
│   ├── fig01_latencia_comparativa.png
│   ├── fig02_nodos_explorados.png
│   ├── fig03_throughput_escalabilidad.png
│   └── fig04_desvio_dinamico_tiempos.png
├── prototipo/
│   ├── nexusnav/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── graph_generator.py
│   │   └── patterns/
│   │       ├── composite.py
│   │       ├── strategy.py
│   │       ├── observer.py
│   │       ├── command.py
│   │       └── iterator.py
│   └── benchmark.py
├── informe/
│   ├── body.md
│   ├── resumen.md
│   ├── referencias.md
│   ├── build_reporte.py
│   ├── convertir_pdf.ps1
│   ├── Informe_Actividad6_Navegando_Mareas.docx
│   └── Informe_Actividad6_Navegando_Mareas.pdf
├── generar_diapositivas.py
├── convertir_pptx_pdf.ps1
└── README.md
```

---

## 🚀 Instrucciones de Ejecución

### Prerrequisitos
- Python 3.10 o superior.
- Dependencias: `pip install matplotlib numpy python-docx pillow pypdf python-pptx`

### 1. Ejecutar la Suite de Pruebas y Benchmarking
```bash
python prototipo/benchmark.py
```

### 2. Renderizar los Modelos UML en PlantUML (Alta Definición 300 DPI)
```bash
python diagramas/render_diagrams.py
```

### 3. Compilar el Informe Técnico Word (.docx) y PDF
```bash
python informe/build_reporte.py
powershell -ExecutionPolicy Bypass -File informe/convertir_pdf.ps1
```

### 4. Generar Presentación de Diapositivas (PowerPoint y PDF)
```bash
python generar_diapositivas.py
powershell -ExecutionPolicy Bypass -File convertir_pptx_pdf.ps1
```

---

## 🎥 Documentación y Recursos

- **Informe Técnico de Arquitectura (PDF, 15 págs):** [`informe/Informe_Actividad6_Navegando_Mareas.pdf`](informe/Informe_Actividad6_Navegando_Mareas.pdf)
- **Repositorio Oficial en GitHub:** [nexusnav-routing-architecture](https://github.com/Alboguaci/nexusnav-routing-architecture)
* **Sustentación en Video:** *(Pendiente de publicación por el equipo)*
