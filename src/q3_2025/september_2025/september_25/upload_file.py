from os import getcwd, listdir
from os.path import splitext
from boto3 import client

# File Path
data_path = getcwd() + "/src/q3_2025/september_2025/september_25/data"

# List of objects
object_list = listdir(data_path)

print(object_list)

# S3 client
s3 = client('s3')

# Loop through the objects
for file in object_list:

    file_name, ext = splitext(file)

    print(file_name)
    print(ext)

    if ext in ['.csv']:

        # Method - .upload_file()
        s3.upload_file(
            f'{data_path}/{file}',
            'dea-test-bucket-september-2025',
            file
        )

        print(f"Uploaded the file: {file} to S3 bucket.")
