# luigi-neo4j-target
A Luigi Target implementation for Neo4j

## Installation

Install the package via pip:

```bash
pip install luigi-neo4j-target
```

## Usage

### Basic usage
```python
from luigi_chromadb_target import ChromaTarget
import neo4j

uri = "bolt://localhost:7687"
driver = neo4j.GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))
target = Neo4jTarget(driver, 'sample_graph')

alice = Node(label="Person", properties={"name": "Alice", "age": 30})
bob = Node(label="Person", properties={"name": "Bob", "age": 25})
friendship = Relationship(start_node=alice, end_node=bob, rel_type="FRIENDS_WITH")

graph = Graph()
graph.add_node(alice)
graph.add_node(bob)
graph.add_relationship(friendship)

target.put(graph)

g = target.get()
print(g)
```

### Advanced options

```python
def my_marshaler(g:str) -> Graph:
    # a logic to transform g string into a Graph
    return Graph

def my_unmarshaler(g:Graph) -> str:
    # a logic to transform Graph g into a string
    return '{my-string-graph-representation}'

target = Neo4jTarget(
    driver,
    'sample_graph',
    marshaler=my_marshaler,
    unmarshaler=my_unmarshaler)

target.put('{my-string-graph-representation}')
```