"""Patrón Command: Encapsulación de acciones de navegación, transacciones y desvíos auditables."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Set, Dict
import time
from ..models import RoutePath, Node
from .composite import RoadSegment, TopologyManager
from .strategy import RoutingEngine


class INavigationCommand(ABC):
    """Interfaz abstracta para el patrón Command."""

    @abstractmethod
    def execute(self) -> Optional[RoutePath]:
        pass

    @abstractmethod
    def undo(self) -> Optional[RoutePath]:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


class NavigateCommand(INavigationCommand):
    """Comando para cálculo y establecimiento de una ruta inicial."""

    def __init__(
        self,
        engine: RoutingEngine,
        topology: TopologyManager,
        origin_id: str,
        destination_id: str
    ):
        self.engine = engine
        self.topology = topology
        self.origin_id = origin_id
        self.destination_id = destination_id
        self.computed_path: Optional[RoutePath] = None

    def execute(self) -> Optional[RoutePath]:
        nodes, segments = self.topology.get_pruned_graph(self.origin_id, self.destination_id)
        self.computed_path = self.engine.compute_route(
            nodes, segments, self.origin_id, self.destination_id
        )
        return self.computed_path

    def undo(self) -> Optional[RoutePath]:
        self.computed_path = None
        return None

    def get_description(self) -> str:
        return f"NavigateCommand: {self.origin_id} -> {self.destination_id}"


class RecalculateDetourCommand(INavigationCommand):
    """Comando para recálculo de desvío ante bloqueo o congestión severa."""

    def __init__(
        self,
        engine: RoutingEngine,
        topology: TopologyManager,
        current_path: RoutePath,
        current_node_id: str,
        blocked_edge_id: str
    ):
        self.engine = engine
        self.topology = topology
        self.previous_path = current_path
        self.current_node_id = current_node_id
        self.blocked_edge_id = blocked_edge_id
        self.detour_path: Optional[RoutePath] = None

    def execute(self) -> Optional[RoutePath]:
        nodes, segments = self.topology.get_pruned_graph(
            self.current_node_id, self.previous_path.destination
        )
        avoid: Set[str] = {self.blocked_edge_id}
        
        # Invalidar entrada de caché para este trayecto
        self.engine.invalidate_cache(avoid)

        # Calcular nuevo tramo evitando el borde congestionado
        detour_subpath = self.engine.compute_route(
            nodes, segments, self.current_node_id, self.previous_path.destination,
            use_cache=False, avoid_edges=avoid
        )

        if not detour_subpath:
            return None

        self.detour_path = detour_subpath
        return self.detour_path

    def undo(self) -> Optional[RoutePath]:
        return self.previous_path

    def get_description(self) -> str:
        return f"RecalculateDetourCommand: desde {self.current_node_id} evitando tramo [{self.blocked_edge_id}]"


class CommandInvoker:
    """Invocador y auditor transaccional con pila de rollback."""

    def __init__(self):
        self._history: List[INavigationCommand] = []
        self._audit_log: List[Dict[str, str]] = []

    def dispatch(self, command: INavigationCommand) -> Optional[RoutePath]:
        start = time.perf_counter()
        result = command.execute()
        duration_ms = (time.perf_counter() - start) * 1000.0

        if result:
            self._history.append(command)
            self._audit_log.append({
                "timestamp": str(time.time()),
                "command": command.get_description(),
                "status": "SUCCESS",
                "duration_ms": f"{duration_ms:.2f} ms",
                "route_id": result.route_id
            })
        else:
            self._audit_log.append({
                "timestamp": str(time.time()),
                "command": command.get_description(),
                "status": "FAILED",
                "duration_ms": f"{duration_ms:.2f} ms",
                "route_id": "NONE"
            })
        return result

    def get_audit_trail(self) -> List[Dict[str, str]]:
        return list(self._audit_log)
