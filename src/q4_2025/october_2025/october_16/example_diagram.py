from diagrams import Diagram, Node, Edge, Cluster

# Context Manager
with Diagram(
    name='',
    filename='test_diagram',
    outformat='pdf'
):
    # Cluster
    with Cluster(label='Simple Diagram'):
        # Create the contents of your diagram
        node_one = Node(label='Node One \n\n\n\n')

        node_two = Node(label='Node Two \n\n\n\n')

        node_one >> Edge(label='Relates To \n\n', color='blue', style='dashed') >> node_two
    
    # Cluster
    with Cluster(label='Simple Diagram 2'):
        # Create the contents of your diagram
        node_three = Node(label='Node Three \n\n\n\n')

        node_four = Node(label='Node Four \n\n\n\n')

        node_three >> Edge(label='Relates To \n\n', color='blue', style='dashed') >> node_four
    
    # Relate some nodes that belong to the two clusters
    node_two >> node_four

