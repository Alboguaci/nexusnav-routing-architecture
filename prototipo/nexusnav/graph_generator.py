"""Generador de topologías urbanas multizona para evaluación experimental de NexusNav."""

import random
from typing import Dict, List, Tuple
from .models import Node
from .patterns.composite import RoadSegment, ZoneCluster, TopologyManager


def build_synthetic_city(
    zones_grid: int = 2, nodes_per_zone: int = 25, seed: int = 42
) -> Tuple[TopologyManager, Dict[str, Node], List[RoadSegment]]:
    """Construye una red urbana sintética multizona con calles locales y corredores arteriales.
    
    Genera una cuadrícula de macro-zonas (por defecto 2x2 = 4 zonas: Norte, Sur, Este, Oeste/Centro).
    Cada zona tiene una cuadrícula interna de calles locales interconectadas.
    Las zonas se conectan mediante corredores arteriales de alta velocidad.
    """
    random.seed(seed)
    topology = TopologyManager()
    all_nodes: Dict[str, Node] = {}
    all_segments: List[RoadSegment] = []

    zone_names = ["Zona_Norte", "Zona_Oriente", "Zona_Occidente", "Zona_Sur"]
    zones_list: List[ZoneCluster] = []

    zone_idx = 0
    zone_side = int(nodes_per_zone ** 0.5)

    for zy in range(zones_grid):
        for zx in range(zones_grid):
            zname = zone_names[zone_idx % len(zone_names)] if zone_idx < len(zone_names) else f"Zona_{zone_idx+1}"
            zid = f"Z{zone_idx+1}"
            zone = ZoneCluster(zid, zname)
            zones_list.append(zone)

            # Offset espacial de la macro-zona
            offset_x = zx * 3000.0  # 3 km entre macrocentros
            offset_y = zy * 3000.0

            # Crear nodos de la zona en grilla
            zone_node_ids: List[List[str]] = []
            for r in range(zone_side):
                row_ids = []
                for c in range(zone_side):
                    nid = f"{zid}_N_{r}_{c}"
                    nx = offset_x + c * 250.0 + random.uniform(-20, 20)  # calles cada 250 m
                    ny = offset_y + r * 250.0 + random.uniform(-20, 20)
                    node = Node(
                        id=nid,
                        x=nx,
                        y=ny,
                        zone_id=zid,
                        name=f"Intersección {zname} {r}-{c}"
                    )
                    all_nodes[nid] = node
                    row_ids.append(nid)
                zone_node_ids.append(row_ids)

            # Crear tramos viales locales horizontales y verticales
            seg_count = 0
            for r in range(zone_side):
                for c in range(zone_side):
                    u_id = zone_node_ids[r][c]
                    u_node = all_nodes[u_id]

                    # Conexión horizontal hacia la derecha
                    if c + 1 < zone_side:
                        v_id = zone_node_ids[r][c + 1]
                        v_node = all_nodes[v_id]
                        dist = u_node.distance_to(v_node)
                        sid = f"SEG_{zid}_H_{r}_{c}"
                        is_art = (r == 2)  # Avenida central horizontal
                        seg = RoadSegment(
                            segment_id=sid,
                            start_node=u_node,
                            end_node=v_node,
                            length_meters=dist,
                            speed_limit_kmh=60.0 if is_art else 40.0,
                            street_name=f"Avenida Central {zname}" if is_art else f"Calle {r*2 + 1} de {zname}",
                            congestion_multiplier=1.0,
                            is_arterial=is_art
                        )
                        zone.add_component(seg)
                        all_segments.append(seg)
                        seg_count += 1

                    # Conexión vertical hacia arriba
                    if r + 1 < zone_side:
                        v_id = zone_node_ids[r + 1][c]
                        v_node = all_nodes[v_id]
                        dist = u_node.distance_to(v_node)
                        sid = f"SEG_{zid}_V_{r}_{c}"
                        is_art = (c == 2)  # Avenida central vertical
                        seg = RoadSegment(
                            segment_id=sid,
                            start_node=u_node,
                            end_node=v_node,
                            length_meters=dist,
                            speed_limit_kmh=60.0 if is_art else 40.0,
                            street_name=f"Carrera Principal {zname}" if is_art else f"Carrera {c*2 + 2} de {zname}",
                            congestion_multiplier=1.0,
                            is_arterial=is_art
                        )
                        zone.add_component(seg)
                        all_segments.append(seg)
                        seg_count += 1

            topology.register_zone(zone)
            zone_idx += 1

    # Crear corredores arteriales inter-zonas (alta velocidad 80 km/h)
    corridor_id = 0
    # Conectar Z1 con Z2 (horizontal superior)
    n1 = all_nodes["Z1_N_2_4"]
    n2 = all_nodes["Z2_N_2_0"]
    c1 = RoadSegment(
        segment_id=f"CORRIDOR_{corridor_id}",
        start_node=n1,
        end_node=n2,
        length_meters=n1.distance_to(n2),
        speed_limit_kmh=80.0,
        street_name="Autopista Norte-Oriente",
        congestion_multiplier=1.0,
        is_arterial=True
    )
    topology.add_corridor(c1)
    all_segments.append(c1)
    corridor_id += 1

    # Conectar Z3 con Z4 (horizontal inferior)
    n3 = all_nodes["Z3_N_2_4"]
    n4 = all_nodes["Z4_N_2_0"]
    c2 = RoadSegment(
        segment_id=f"CORRIDOR_{corridor_id}",
        start_node=n3,
        end_node=n4,
        length_meters=n3.distance_to(n4),
        speed_limit_kmh=80.0,
        street_name="Avenida Longitudinal Sur",
        congestion_multiplier=1.0,
        is_arterial=True
    )
    topology.add_corridor(c2)
    all_segments.append(c2)
    corridor_id += 1

    # Conectar Z1 con Z3 (vertical izquierdo)
    n5 = all_nodes["Z1_N_4_2"]
    n6 = all_nodes["Z3_N_0_2"]
    c3 = RoadSegment(
        segment_id=f"CORRIDOR_{corridor_id}",
        start_node=n5,
        end_node=n6,
        length_meters=n5.distance_to(n6),
        speed_limit_kmh=80.0,
        street_name="Corredor Transversal Central",
        congestion_multiplier=1.0,
        is_arterial=True
    )
    topology.add_corridor(c3)
    all_segments.append(c3)
    corridor_id += 1

    # Conectar Z2 con Z4 (vertical derecho)
    n7 = all_nodes["Z2_N_4_2"]
    n8 = all_nodes["Z4_N_0_2"]
    c4 = RoadSegment(
        segment_id=f"CORRIDOR_{corridor_id}",
        start_node=n7,
        end_node=n8,
        length_meters=n7.distance_to(n8),
        speed_limit_kmh=80.0,
        street_name="Avenida Circunvalar Oriente",
        congestion_multiplier=1.0,
        is_arterial=True
    )
    topology.add_corridor(c4)
    all_segments.append(c4)

    return topology, all_nodes, all_segments
