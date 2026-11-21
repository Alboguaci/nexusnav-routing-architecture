"""Modelos de datos fundamentales para NexusNav."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional


@dataclass
class Node:
    """Representa una intersección o nodo vial en el grafo espacial."""
    id: str
    x: float
    y: float
    zone_id: str
    name: str = ""

    def distance_to(self, other: Node) -> float:
        """Distancia euclidiana entre dos nodos (metros)."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass
class ManeuverStep:
    """Instrucción atómica de navegación para el conductor o cliente telemático."""
    instruction: str
    distance_meters: float
    estimated_seconds: float
    target_street: str
    turn_direction: str  # 'straight', 'left', 'right', 'u-turn', 'destination'
    node_id: str


@dataclass
class RoutePath:
    """Agregado que encapsula la ruta óptima calculada."""
    route_id: str
    origin: str
    destination: str
    nodes: List[str]
    edges: List[str]
    total_distance_meters: float
    total_time_seconds: float
    maneuvers: List[ManeuverStep] = field(default_factory=list)
    strategy_used: str = ""
    nodes_explored_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def get_edges(self) -> List[str]:
        return list(self.edges)


@dataclass
class TrafficIncidentEvent:
    """Evento asíncrono emitido por sensores o telemetría urbana."""
    event_id: str
    edge_id: str
    severity: str  # 'LOW', 'MEDIUM', 'HIGH', 'BLOCKED'
    delay_multiplier: float  # Factor de multiplicación sobre el tiempo base (e.g. 3.5x)
    description: str
    timestamp: datetime = field(default_factory=datetime.now)
