from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class Node:
    """
    Represents a node (vertex) in the graph.
    """
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return f'()'

    def __hash__(self):
        return hash((self.label, frozenset(self.properties.items())))


@dataclass
class Relationship:
    """
    Represents a relationship (edge) between two nodes in the graph.
    """
    start_node: Node
    end_node: Node
    rel_type: str = "RELATED_TO"

    def __hash__(self):
        return hash((self.start_node, self.end_node, self.rel_type))


@dataclass
class Graph:
    """
    Represents a graph that contains nodes and relationships.
    """
    nodes: List[Node] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)

    def add_node(self, node: Node):
        """
        Adds a node to the graph if it doesn't already exist.
        """
        if node not in self.nodes:
            self.nodes.append(node)

    def add_relationship(self, relationship: Relationship):
        """
        Adds a relationship to the graph, ensuring the nodes exist.
        """
        self.add_node(relationship.start_node)
        self.add_node(relationship.end_node)
        
        if relationship not in self.relationships:
            self.relationships.append(relationship)

    def to_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Converts the graph into a dictionary format suitable for Neo4jTarget.
        """
        nodes_dict = [
            {"label": node.label, "properties": node.properties}
            for node in self.nodes
        ]
        relationships_dict = [
            {
                "start": relationship.start_node.properties.get("name", ""),
                "end": relationship.end_node.properties.get("name", ""),
                "type": relationship.rel_type
            }
        for relationship in self.relationships]
        
        return {"nodes": nodes_dict, "relationships": relationships_dict}
