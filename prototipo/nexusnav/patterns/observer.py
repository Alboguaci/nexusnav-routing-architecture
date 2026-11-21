"""Patrón Observer: Telemetría asíncrona y detección proactiva de incidentes de tráfico."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Set, Optional, Callable
from ..models import TrafficIncidentEvent, RoutePath


class ITrafficObserver(ABC):
    """Interfaz observadora para componentes interesados en variaciones de tráfico."""

    @abstractmethod
    def on_traffic_event(self, event: TrafficIncidentEvent) -> None:
        """Callback invocado cuando ocurre un incidente en un tramo vial suscrito."""
        pass

    @abstractmethod
    def get_id(self) -> str:
        """Identificador de la entidad observadora."""
        pass


class ITrafficSubject(ABC):
    """Interfaz del Sujeto (Subject) para el patrón Observer."""

    @abstractmethod
    def register_observer(self, observer: ITrafficObserver, edge_ids: List[str]) -> None:
        pass

    @abstractmethod
    def remove_observer(self, observer: ITrafficObserver) -> None:
        pass

    @abstractmethod
    def publish_incident(self, event: TrafficIncidentEvent) -> None:
        pass


class TrafficEventBus(ITrafficSubject):
    """Bus de eventos centralizado con filtrado selectivo O(K) por tramo vial."""

    def __init__(self):
        # Mapeo: edge_id -> Set[ITrafficObserver]
        self._subscriptions: Dict[str, Set[ITrafficObserver]] = {}
        self.published_events_count = 0
        self.dispatched_notifications_count = 0

    def register_observer(self, observer: ITrafficObserver, edge_ids: List[str]) -> None:
        for edge in edge_ids:
            if edge not in self._subscriptions:
                self._subscriptions[edge] = set()
            self._subscriptions[edge].add(observer)

    def remove_observer(self, observer: ITrafficObserver) -> None:
        for edge, observers in self._subscriptions.items():
            observers.discard(observer)

    def update_observer_edges(
        self, observer: ITrafficObserver, old_edges: List[str], new_edges: List[str]
    ) -> None:
        """Actualiza granularmente la suscripción tras un desvío o recálculo."""
        for old in old_edges:
            if old in self._subscriptions:
                self._subscriptions[old].discard(observer)
        for new in new_edges:
            if new not in self._subscriptions:
                self._subscriptions[new] = set()
            self._subscriptions[new].add(observer)

    def publish_incident(self, event: TrafficIncidentEvent) -> None:
        """Notifica única y exclusivamente a los observadores que contienen el tramo afectado."""
        self.published_events_count += 1
        subscribers = self._subscriptions.get(event.edge_id, set())
        for obs in list(subscribers):
            obs.on_traffic_event(event)
            self.dispatched_notifications_count += 1


class RouteMonitorObserver(ITrafficObserver):
    """Observador asignado a una sesión de viaje vehicular activa."""

    def __init__(
        self,
        session_id: str,
        current_route: RoutePath,
        reroute_callback: Callable[[RoutePath, str], Optional[RoutePath]],
        reroute_threshold_seconds: float = 120.0
    ):
        self.session_id = session_id
        self.current_route = current_route
        self.reroute_callback = reroute_callback
        self.reroute_threshold_seconds = reroute_threshold_seconds
        self.incidents_encountered: List[TrafficIncidentEvent] = []
        self.reroutes_triggered = 0

    def get_id(self) -> str:
        return self.session_id

    def on_traffic_event(self, event: TrafficIncidentEvent) -> None:
        self.incidents_encountered.append(event)

        # Evaluar impacto del incidente sobre el tiempo restante
        # Supongamos que el tramo demora multiplier * base
        base_estimate = 30.0  # estimación promedio de tramo
        estimated_delay = (event.delay_multiplier - 1.0) * base_estimate

        if estimated_delay >= self.reroute_threshold_seconds or event.severity == "BLOCKED":
            # Demora severa: Disparar recálculo proactivo de desvío
            new_path = self.reroute_callback(self.current_route, event.edge_id)
            if new_path:
                self.current_route = new_path
                self.reroutes_triggered += 1
