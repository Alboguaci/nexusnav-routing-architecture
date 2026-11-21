"""Patrón Composite: Estructuración jerárquica de la topología vial urbana."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Set, Optional, Tuple
from ..models import Node


class INetworkComponent(ABC):
    """Interfaz común para el patrón Composite."""

    @abstractmethod
    def get_id(self) -> str:
        """Identificador único del componente."""
        pass

    @abstractmethod
    def get_total_length(self) -> float:
        """Longitud total en metros."""
        pass

    @abstractmethod
    def contains_node(self, node_id: str) -> bool:
        """Verifica si el nodo pertenece a este componente jerárquico."""
        pass

    @abstractmethod
    def collect_nodes(self) -> Dict[str, Node]:
        """Recolecta todos los nodos contenidos."""
        pass

    @abstractmethod
    def collect_segments(self) -> List[RoadSegment]:
        """Recolecta todos los segmentos viales hoja."""
        pass


class RoadSegment(INetworkComponent):
    """Elemento Hoja (Leaf) del patrón Composite: representa un tramo vial unívoco."""

    def __init__(
        self,
        segment_id: str,
        start_node: Node,
        end_node: Node,
        length_meters: float,
        speed_limit_kmh: float = 50.0,
        street_name: str = "Calle Local",
        congestion_multiplier: float = 1.0,
        is_arterial: bool = False
    ):
        self.segment_id = segment_id
        self.start_node = start_node
        self.end_node = end_node
        self.length_meters = length_meters
        self.speed_limit_kmh = speed_limit_kmh
        self.street_name = street_name
        self.congestion_multiplier = congestion_multiplier
        self.is_arterial = is_arterial

    def get_id(self) -> str:
        return self.segment_id

    def get_total_length(self) -> float:
        return self.length_meters

    def contains_node(self, node_id: str) -> bool:
        return self.start_node.id == node_id or self.end_node.id == node_id

    def collect_nodes(self) -> Dict[str, Node]:
        return {self.start_node.id: self.start_node, self.end_node.id: self.end_node}

    def collect_segments(self) -> List[RoadSegment]:
        return [self]

    def get_travel_time_seconds(self) -> float:
        """Calcula el tiempo de viaje considerando el factor de congestión dinámico."""
        speed_mps = (self.speed_limit_kmh * 1000.0) / 3600.0
        effective_speed = max(1.0, speed_mps / self.congestion_multiplier)
        return self.length_meters / effective_speed


class ZoneCluster(INetworkComponent):
    """Elemento Compuesto (Composite): representa un macro-sector urbano (distrito/comuna)."""

    def __init__(self, zone_id: str, zone_name: str):
        self.zone_id = zone_id
        self.zone_name = zone_name
        self._children: List[INetworkComponent] = []
        self._cached_nodes: Optional[Dict[str, Node]] = None

    def add_component(self, component: INetworkComponent) -> None:
        self._children.append(component)
        self._cached_nodes = None

    def remove_component(self, component: INetworkComponent) -> None:
        self._children.remove(component)
        self._cached_nodes = None

    def get_id(self) -> str:
        return self.zone_id

    def get_total_length(self) -> float:
        return sum(child.get_total_length() for child in self._children)

    def contains_node(self, node_id: str) -> bool:
        return any(child.contains_node(node_id) for child in self._children)

    def collect_nodes(self) -> Dict[str, Node]:
        if self._cached_nodes is None:
            nodes: Dict[str, Node] = {}
            for child in self._children:
                nodes.update(child.collect_nodes())
            self._cached_nodes = nodes
        return self._cached_nodes

    def collect_segments(self) -> List[RoadSegment]:
        segments: List[RoadSegment] = []
        for child in self._children:
            segments.extend(child.collect_segments())
        return segments

    def get_centroid(self) -> Tuple[float, float]:
        """Calcula las coordenadas promedio (centroide) del macro-sector."""
        nodes = self.collect_nodes()
        if not nodes:
            return (0.0, 0.0)
        avg_x = sum(n.x for n in nodes.values()) / len(nodes)
        avg_y = sum(n.y for n in nodes.values()) / len(nodes)
        return (avg_x, avg_y)


class TopologyManager:
    """Administrador topológico que orquesta la poda y consulta espacial de subgrafos."""

    def __init__(self):
        self.zones: Dict[str, ZoneCluster] = {}
        self.inter_zone_corridors: List[RoadSegment] = []

    def register_zone(self, zone: ZoneCluster) -> None:
        self.zones[zone.zone_id] = zone

    def add_corridor(self, corridor: RoadSegment) -> None:
        self.inter_zone_corridors.append(corridor)

    def find_zone_for_node(self, node_id: str) -> Optional[str]:
        for zone_id, zone in self.zones.items():
            if zone.contains_node(node_id):
                return zone_id
        return None

    def get_pruned_graph(
        self, origin_id: str, destination_id: str
    ) -> Tuple[Dict[str, Node], List[RoadSegment]]:
        """Poda topológica: extrae únicamente las macrozonas relevantes y los corredores arteriales.
        
        Si el origen y el destino están en la misma zona, retorna exclusivamente el subgrafo local.
        Si están en zonas distintas, incluye las dos zonas involucradas y las arterias conectoras,
        podando todas las calles capilares de zonas intermedias ajenas.
        """
        origin_zone = self.find_zone_for_node(origin_id)
        dest_zone = self.find_zone_for_node(destination_id)

        selected_nodes: Dict[str, Node] = {}
        selected_segments: List[RoadSegment] = []

        if origin_zone and dest_zone and origin_zone == dest_zone:
            # Misma zona: poda masiva de todo el resto de la ciudad
            local_zone = self.zones[origin_zone]
            selected_nodes.update(local_zone.collect_nodes())
            selected_segments.extend(local_zone.collect_segments())
        else:
            # Zonas diferentes: incluir zona origen completa, zona destino completa,
            # y la red arterial (avenidas principales y corredores) de las zonas intermedias
            if origin_zone and origin_zone in self.zones:
                selected_nodes.update(self.zones[origin_zone].collect_nodes())
                selected_segments.extend(self.zones[origin_zone].collect_segments())
            if dest_zone and dest_zone in self.zones:
                selected_nodes.update(self.zones[dest_zone].collect_nodes())
                selected_segments.extend(self.zones[dest_zone].collect_segments())
            
            # Incorporar tramos arteriales de las demás zonas (sin calles capilares residenciales)
            for zid, zone in self.zones.items():
                if zid != origin_zone and zid != dest_zone:
                    for seg in zone.collect_segments():
                        if seg.is_arterial:
                            selected_segments.append(seg)
                            selected_nodes[seg.start_node.id] = seg.start_node
                            selected_nodes[seg.end_node.id] = seg.end_node

            # Incorporar corredores inter-zonales
            for corridor in self.inter_zone_corridors:
                selected_segments.append(corridor)
                selected_nodes[corridor.start_node.id] = corridor.start_node
                selected_nodes[corridor.end_node.id] = corridor.end_node

        return selected_nodes, selected_segments
