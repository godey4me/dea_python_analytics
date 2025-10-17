from os import getcwd
from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.programming.language import Python
from diagrams.custom import Custom

# Icon Path
icon_path = getcwd() + "/src/q4_2025/october_2025/october_16/icons"

# Diagram
with Diagram(filename='aws_etl', outformat='pdf', graph_attr={'bgcolor': 'black'}):

    # Cluster
    with Cluster(label='AWS Workflow'):

        # Inner Clusters
        with Cluster(label='Storage'):

            # s3 Node
            s3 = S3('Bucket')

            # Custom Node - CSV files
            csv_icon = Custom(label='CSV \n Files', icon_path=f'{icon_path}/csv_icon.png')

            s3 >> csv_icon
        
        # Cluster for Python workflow
        with Cluster(label='Python Workflow'):

            # Python logo
            python_node = Python(label='etl.py')

            # Custom logo for Pandas
            pandas_node = Custom(label='DataFrame', icon_path=f'{icon_path}/pandas_logo.png')

            python_node >> pandas_node
        
        rds_node = RDSPostgresqlInstance(label='PostgreSQL')
        
        csv_icon >> python_node
        pandas_node >> rds_node

