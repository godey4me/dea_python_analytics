## Diagrams Module in Python

### Description

- Diagrams allows you to create diagrams with code using Python. It is a great alternative to build system level diagrams in lieu of enteprise visualization tools.

### Setup

1. `diagrams` uses `graphviz` as a dependency in order to work so you have to install `graphviz` on your operating system.

#### Windows

- Windows 11 - Use `winget`

1. Go to [Winget](https://winget.run)
2. Search for `Graphviz`.
3. Click on `Copy command`
4. Paste the command in a Terminal.

- Windows 10 - Use `chocolatey`

1. Within an Administrator Command Prompt, type in the following command:

```bash
choco install graphviz
```

- Mac - Use Homebrew

1. Within a Terminal, use the following command:

```bash
brew install graphviz
```

2. Install the following packages using `pip`

```txt
graphviz
diagrams
```

- Within a Terminal, type in the following command:

```bash
pip install -r requirements.txt
```

### Basic Usage

- Diagrams essentially operates on a graph structure which means that you have nodes, edges, and clusters.

- A diagram has its own context which means you have to use the word `with` to manage whatever happens inside the diagram.
- Same is true for clusters that are inside the diagram.

- Use the `>>` between nodes to create relationships between the nodes.

```python
from diagrams import Diagram, Node, Edge

with Diagram():
    # Manage the context
    node_one = Node(label='node_one')
    node_two = Node(label='node_two')

    node_one >> node_two
```

- If you want specialized logos for aspects such as the cloud or open source software, you can get all the logos from the official documentation.
    - Resource linked below.

### Resources

- [Official Documentation - Diagrams as Code](https://diagrams.mingrammer.com/)