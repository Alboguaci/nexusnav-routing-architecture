"""Patrón Strategy: Desacoplamiento de algoritmos de enrutamiento y optimización de trayectorias."""

from __future__ import annotations
from abc import ABC, abstractmethod
import heapq
import math
import time
from typing import Dict, List, Tuple, Optional, Set
from ..models import Node, RoutePath, ManeuverStep
from .composite import RoadSegment


class IRoutingStrategy(ABC):
    """Interfaz para la familia de algoritmos de enrutamiento intercambiables."""

    @abstractmethod
    def calculate_route(
        self,
        nodes: Dict[str, Node],
        segments: List[RoadSegment],
        origin_id: str,
        destination_id: str,
        avoid_edges: Optional[Set[str]] = None
    ) -> Optional[RoutePath]:
        """Calcula la ruta óptima según el criterio y lógica de la estrategia concreta."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Nombre formal de la estrategia."""
        pass


def _build_adjacency_list(
    segments: List[RoadSegment], avoid_edges: Optional[Set[str]] = None
) -> Dict[str, List[Tuple[str, float, float, RoadSegment]]]:
    """Construye lista de adyacencia: node -> [(neighbor, travel_time, length, segment)]."""
    adj: Dict[str, List[Tuple[str, float, float, RoadSegment]]] = {}
    avoid = avoid_edges or set()

    for seg in segments:
        if seg.segment_id in avoid:
            continue
        u = seg.start_node.id
        v = seg.end_node.id
        t = seg.get_travel_time_seconds()
        d = seg.length_meters

        # Calles de doble sentido o sentido único
        if u not in adj:
            adj[u] = []
        adj[u].append((v, t, d, seg))

        if v not in adj:
            adj[v] = []
        adj[v].append((u, t, d, seg))

    return adj


def _generate_maneuvers(
    path_nodes: List[str], path_segments: List[RoadSegment], nodes_map: Dict[str, Node]
) -> List[ManeuverStep]:
    """Genera instrucciones paso a paso a partir de la secuencia geométrica."""
    maneuvers: List[ManeuverStep] = []
    if len(path_nodes) < 2:
        return maneuvers

    for i in range(len(path_segments)):
        seg = path_segments[i]
        curr_node = nodes_map.get(path_nodes[i])
        next_node = nodes_map.get(path_nodes[i + 1])
        target_name = seg.street_name

        if i == 0:
            instruction = f"Inicie su recorrido en {curr_node.name or curr_node.id} por {target_name}"
            turn = "straight"
        elif i == len(path_segments) - 1:
            instruction = f"Avance por {target_name} hasta su destino final en {next_node.name or next_node.id}"
            turn = "destination"
        else:
            # Determinación simplificada de giro según cambio de calle
            prev_seg = path_segments[i - 1]
            if prev_seg.street_name != seg.street_name:
                instruction = f"Gire hacia {target_name}"
                turn = "turn"
            else:
                instruction = f"Continúe recto por {target_name}"
                turn = "straight"

        maneuvers.append(
            ManeuverStep(
                instruction=instruction,
                distance_meters=round(seg.length_meters, 1),
                estimated_seconds=round(seg.get_travel_time_seconds(), 1),
                target_street=target_name,
                turn_direction=turn,
                node_id=next_node.id if next_node else ""
            )
        )
    return maneuvers


class DijkstraRoutingStrategy(IRoutingStrategy):
    """Estrategia de Enrutamiento Exacto: Algoritmo de Dijkstra estándar sin heurística."""

    def calculate_route(
        self,
        nodes: Dict[str, Node],
        segments: List[RoadSegment],
        origin_id: str,
        destination_id: str,
        avoid_edges: Optional[Set[str]] = None
    ) -> Optional[RoutePath]:
        if origin_id not in nodes or destination_id not in nodes:
            return None

        adj = _build_adjacency_list(segments, avoid_edges)
        distances: Dict[str, float] = {nid: float("inf") for nid in nodes}
        distances[origin_id] = 0.0
        predecessors: Dict[str, Tuple[Optional[str], Optional[RoadSegment]]] = {
            origin_id: (None, None)
        }

        # Cola de prioridad: (costo_acumulado_tiempo, node_id)
        pq: List[Tuple[float, str]] = [(0.0, origin_id)]
        visited: Set[str] = set()
        explored_count = 0

        while pq:
            curr_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            explored_count += 1

            if u == destination_id:
                break

            for v, travel_time, length, seg in adj.get(u, []):
                if v in visited:
                    continue
                new_cost = curr_dist + travel_time
                if new_cost < distances.get(v, float("inf")):
                    distances[v] = new_cost
                    predecessors[v] = (u, seg)
                    heapq.heappush(pq, (new_cost, v))

        if distances.get(destination_id, float("inf")) == float("inf"):
            return None

        # Reconstruir camino
        curr = destination_id
        path_nodes: List[str] = []
        path_segments: List[RoadSegment] = []
        while curr is not None:
            path_nodes.append(curr)
            prev_node, seg = predecessors[curr]
            if seg:
                path_segments.append(seg)
            curr = prev_node

        path_nodes.reverse()
        path_segments.reverse()

        total_distance = sum(s.length_meters for s in path_segments)
        total_time = distances[destination_id]
        maneuvers = _generate_maneuvers(path_nodes, path_segments, nodes)

        return RoutePath(
            route_id=f"rt-dijkstra-{int(time.time() * 1000)}",
            origin=origin_id,
            destination=destination_id,
            nodes=path_nodes,
            edges=[s.segment_id for s in path_segments],
            total_distance_meters=round(total_distance, 1),
            total_time_seconds=round(total_time, 2),
            maneuvers=maneuvers,
            strategy_used="Dijkstra Exact",
            nodes_explored_count=explored_count
        )

    def get_name(self) -> str:
        return "Dijkstra Exact"


class AStarRoutingStrategy(IRoutingStrategy):
    """Estrategia A*: Búsqueda heurística informada para minimización de tiempo de viaje."""

    def __init__(self, max_speed_kmh: float = 80.0):
        self.max_speed_mps = (max_speed_kmh * 1000.0) / 3600.0

    def _heuristic_time(self, u_node: Node, target_node: Node) -> float:
        """Heurística admisible: tiempo mínimo a velocidad máxima teórica en línea recta."""
        dist = u_node.distance_to(target_node)
        return dist / self.max_speed_mps

    def calculate_route(
        self,
        nodes: Dict[str, Node],
        segments: List[RoadSegment],
        origin_id: str,
        destination_id: str,
        avoid_edges: Optional[Set[str]] = None
    ) -> Optional[RoutePath]:
        if origin_id not in nodes or destination_id not in nodes:
            return None

        target_node = nodes[destination_id]
        adj = _build_adjacency_list(segments, avoid_edges)

        g_score: Dict[str, float] = {nid: float("inf") for nid in nodes}
        g_score[origin_id] = 0.0

        f_score: Dict[str, float] = {nid: float("inf") for nid in nodes}
        f_score[origin_id] = self._heuristic_time(nodes[origin_id], target_node)

        predecessors: Dict[str, Tuple[Optional[str], Optional[RoadSegment]]] = {
            origin_id: (None, None)
        }

        # Priority Queue: (f_score, node_id)
        open_set: List[Tuple[float, str]] = [(f_score[origin_id], origin_id)]
        open_set_hash: Set[str] = {origin_id}
        closed_set: Set[str] = set()
        explored_count = 0

        while open_set:
            _, u = heapq.heappop(open_set)
            open_set_hash.discard(u)

            if u in closed_set:
                continue
            closed_set.add(u)
            explored_count += 1

            if u == destination_id:
                break

            curr_g = g_score[u]
            u_node = nodes[u]

            for v, travel_time, length, seg in adj.get(u, []):
                if v in closed_set:
                    continue

                tentative_g = curr_g + travel_time
                if tentative_g < g_score.get(v, float("inf")):
                    g_score[v] = tentative_g
                    v_node = nodes[v]
                    h_val = self._heuristic_time(v_node, target_node)
                    f_val = tentative_g + h_val
                    f_score[v] = f_val
                    predecessors[v] = (u, seg)

                    if v not in open_set_hash:
                        open_set_hash.add(v)
                        heapq.heappush(open_set, (f_val, v))

        if g_score.get(destination_id, float("inf")) == float("inf"):
            return None

        # Reconstruir camino
        curr = destination_id
        path_nodes: List[str] = []
        path_segments: List[RoadSegment] = []
        while curr is not None:
            path_nodes.append(curr)
            prev_node, seg = predecessors[curr]
            if seg:
                path_segments.append(seg)
            curr = prev_node

        path_nodes.reverse()
        path_segments.reverse()

        total_distance = sum(s.length_meters for s in path_segments)
        total_time = g_score[destination_id]
        maneuvers = _generate_maneuvers(path_nodes, path_segments, nodes)

        return RoutePath(
            route_id=f"rt-astar-{int(time.time() * 1000)}",
            origin=origin_id,
            destination=destination_id,
            nodes=path_nodes,
            edges=[s.segment_id for s in path_segments],
            total_distance_meters=round(total_distance, 1),
            total_time_seconds=round(total_time, 2),
            maneuvers=maneuvers,
            strategy_used="A* Dynamic Heuristic",
            nodes_explored_count=explored_count
        )

    def get_name(self) -> str:
        return "A* Dynamic Heuristic"


class RoutingEngine:
    """Contexto del Patrón Strategy con soporte integrado de caché espacial (LRU/TTL)."""

    def __init__(self, default_strategy: Optional[IRoutingStrategy] = None, cache_ttl_seconds: float = 60.0):
        self._strategy: IRoutingStrategy = default_strategy or AStarRoutingStrategy()
        self._cache: Dict[Tuple[str, str], Tuple[RoutePath, float]] = {}
        self._cache_ttl = cache_ttl_seconds
        self.cache_hits = 0
        self.cache_misses = 0

    def set_strategy(self, strategy: IRoutingStrategy) -> None:
        self._strategy = strategy

    def get_strategy(self) -> IRoutingStrategy:
        return self._strategy

    def invalidate_cache(self, affected_edges: Optional[Set[str]] = None) -> None:
        """Invalida entradas de caché que contengan los tramos afectados por congestión."""
        if not affected_edges:
            self._cache.clear()
            return

        keys_to_remove = []
        for key, (path, _) in self._cache.items():
            if any(e in affected_edges for e in path.edges):
                keys_to_remove.append(key)
        for k in keys_to_remove:
            del self._cache[k]

    def compute_route(
        self,
        nodes: Dict[str, Node],
        segments: List[RoadSegment],
        origin_id: str,
        destination_id: str,
        use_cache: bool = True,
        avoid_edges: Optional[Set[str]] = None
    ) -> Optional[RoutePath]:
        key = (origin_id, destination_id)
        now = time.time()

        if use_cache and not avoid_edges and key in self._cache:
            path, timestamp = self._cache[key]
            if now - timestamp < self._cache_ttl:
                self.cache_hits += 1
                return path

        self.cache_misses += 1
        path = self._strategy.calculate_route(nodes, segments, origin_id, destination_id, avoid_edges)

        if path and use_cache and not avoid_edges:
            self._cache[key] = (path, now)

        return path
