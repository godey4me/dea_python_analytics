from os import getcwd, environ
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Path to the .env file
env_path = getcwd() + "/src/q4_2025/october_2025/october_2/.env"

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

# Create a blob client
blob_client = container.get_blob_client('international_education_costs.csv')

# CSV file path
csv_path = getcwd() + "/data/csv_files/International_Education_Costs.csv"

with open(csv_path, "rb") as buffer:
    # Upload
    blob_client.upload_blob(data=buffer, overwrite=True)

print("New blob uploaded to container.")