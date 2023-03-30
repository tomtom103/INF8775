from typing import Dict, Optional, List, Iterator, Tuple

class Vertex: # Sommet
    def __init__(self, node: int, size: int) -> None:
        self.id = node
        self.size = size
        self.adjacent: Dict["Vertex", int] = {}

    def __str__(self) -> str:
        return f"{self.id} adjacent: {str([x.id for x in self.adjacent])}"
    
    def __hash__(self) -> int:
        return hash(str(self.id))
    
    def __eq__(self, other: "Vertex") -> bool:
        return self.id == other.id and self.size == other.size

    def add_neighbor(self, neighbor: "Vertex", weight: int = 0):
        self.adjacent[neighbor] = weight

    def get_connections(self) -> List["Vertex"]:
        return list(self.adjacent.keys())
    
    def get_weight(self, neighbor: "Vertex") -> int:
        return self.adjacent.get(neighbor, 0)


class Graph:
    def __init__(self) -> None:
        self.vertices: Dict[int, Vertex] = {}
        self.n_vertices = 0

    def __iter__(self) -> Iterator[Vertex]:
        return iter(self.vertices.values())

    def add_vertex(self, node: int, size: int) -> Vertex: # Ajout arrete
        self.n_vertices += 1
        vertex = Vertex(node, size)
        self.vertices[node] = vertex
        return vertex
    
    def get_vertex(self, node: int) -> Optional[Vertex]:
        return self.vertices.get(node, None)
    
    def add_edge(self, from_id: int, to_id: int, cost: int = 0) -> None:
        # All possible vertices must be inserted before this is called
        self.vertices[from_id].add_neighbor(self.vertices[to_id], cost)

    def get_vertices(self) -> List[int]:
        return list(self.vertices.keys())

