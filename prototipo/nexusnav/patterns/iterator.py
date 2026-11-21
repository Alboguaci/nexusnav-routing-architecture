"""Patrón Iterator: Travesía secuencial desacoplada de instrucciones y maniobras de navegación."""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, List
from ..models import ManeuverStep, RoutePath


class IRouteIterator(ABC):
    """Interfaz abstracta del iterador de navegación."""

    @abstractmethod
    def has_next(self) -> bool:
        """Indica si existen más maniobras pendientes en el recorrido."""
        pass

    @abstractmethod
    def next(self) -> ManeuverStep:
        """Retorna la siguiente maniobra y avanza el cursor."""
        pass

    @abstractmethod
    def current(self) -> Optional[ManeuverStep]:
        """Consulta la maniobra actual sin avanzar."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reinicia el cursor al inicio de la ruta."""
        pass

    @abstractmethod
    def remaining_count(self) -> int:
        """Cantidad de maniobras restantes."""
        pass


class ManeuverIterator(IRouteIterator):
    """Iterador concreto para consumir secuencialmente los pasos de una ruta calculada."""

    def __init__(self, route_path: RoutePath):
        self._route_path = route_path
        self._cursor: int = 0

    def has_next(self) -> bool:
        return self._cursor < len(self._route_path.maneuvers)

    def next(self) -> ManeuverStep:
        if not self.has_next():
            raise StopIteration("No hay más maniobras disponibles en la ruta.")
        step = self._route_path.maneuvers[self._cursor]
        self._cursor += 1
        return step

    def current(self) -> Optional[ManeuverStep]:
        if 0 <= self._cursor < len(self._route_path.maneuvers):
            return self._route_path.maneuvers[self._cursor]
        return None

    def reset(self) -> None:
        self._cursor = 0

    def remaining_count(self) -> int:
        return max(0, len(self._route_path.maneuvers) - self._cursor)

    def update_route_path(self, new_route: RoutePath, match_node_id: Optional[str] = None) -> None:
        """Actualiza la ruta en caliente (por ejemplo tras un recálculo por desvío)
        y sincroniza el cursor al nodo actual del vehículo.
        """
        self._route_path = new_route
        self._cursor = 0
        if match_node_id:
            for i, step in enumerate(new_route.maneuvers):
                if step.node_id == match_node_id:
                    self._cursor = i
                    break
