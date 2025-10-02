import pandas as pd
from os import getcwd, environ
from io import BytesIO
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Path to the .env file
env_path = getcwd() + "/src/q4_2025/october_2025/october_2/new.env"

# Load environment variables
load_dotenv(env_path)

# Get the connection string from environment variables
conn_str = environ.get('AZURE_STORAGE_CONNECTION_STRING')

# Generate the service
service = BlobServiceClient.from_connection_string(conn_str)

# Name of container
container_name = "csv-files"

# Access the specific container containing your CSV blobs
container = service.get_container_client(container_name)

# Dictionary of DataFrames
df_dict = {}

# Iterate through the blobs in each container
for blob in container.list_blobs():
    # Check if the blob is a CSV file
    if blob.name.lower().endswith(".csv"):
        print(f"Found: {blob.name}")

        # Create a blob client for each blob name
        blob_client = container.get_blob_client(blob=blob.name)

        # Get the stream
        stream = blob_client.download_blob()

        # Data in bytes
        data_bytes = stream.readall()

        # DataFrame
        df = pd.read_csv(BytesIO(data_bytes))

        # Update our dictionary
        df_dict[blob.name] = df

        print(f"Retrieved contents from {blob.name} and generated a DataFrame.")
    
        df.info()
        print(df.head())

        print("-"*50)