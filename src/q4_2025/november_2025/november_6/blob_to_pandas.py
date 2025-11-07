import pandas as pd
from os import getcwd, environ
from io import BytesIO
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Custom modules
from fmt_util import line_separator

# Path to the .env file
env_path = getcwd() + "/src/q4_2025/october_2025/october_2/new.env"

# Load environment variables
load_dotenv(env_path)

# Get the connection string from environment variables
conn_str = environ.get('AZURE_STORAGE_CONNECTION_STRING')

# Generate the service
service = BlobServiceClient.from_connection_string(conn_str)

# Name of container
container_name = "parquet-files"

# Access the specific container containing your CSV blobs
container = service.get_container_client(container_name)

print("Retrieved container client.")

line_separator()

blob_list = list(container.list_blob_names())

print(blob_list)

line_separator()

blobs_to_download = []

# Iterate through the blobs in each container
for blob in container.list_blobs():
    # Check if the blob is a CSV file
    if blob.name.lower().endswith(".parquet"):
        print(f"Found: {blob.name}")
        blobs_to_download.append(blob.name)

# Dictionary
blob_df_dict = {}

# Loop
for blob_name in blobs_to_download:
    # Create a client specifically for the blob
    blob_client = container.get_blob_client(blob_name)

    # Get the contents as a storage stream which is Microsoft's custom buffer
    stream = blob_client.download_blob()

    # Get the data in bytes
    data_bytes = stream.readall()

    # DataFrame
    df = pd.read_parquet(BytesIO(data_bytes))

    # Information of the DataFrame
    df.info()

    # Add a key, value pair
    blob_df_dict[blob_name] = df

# Get the final DataFrame
final_df = blob_df_dict['web_photos_table.parquet']

final_df.info()