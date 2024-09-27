from pydantic.dataclasses import dataclass


@dataclass
class Node:
    name: str
    config: dict
    type: str


@dataclass
class Relationship:
    src_node_name: str
    src_node_type: str
    dest_node_name: str
    dest_node_type: str
    type: str


@dataclass
class Destination:
    node_element_id: str
    node_name: str
    node_type: str
    relationship_type: str


@dataclass
class SimilaritySearchMetadata:
    score: float
    node_labels: list
    id: str


@dataclass
class NodeSimilaritySearchResult:
    node: Node
    metadata: SimilaritySearchMetadata
