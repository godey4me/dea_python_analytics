# Getting Started with AWS CLI and boto3 for S3

## Description
This guide will help you set up your AWS account, configure the AWS CLI, and use `boto3` (the AWS SDK for Python) to interact with Amazon S3. By the end, you’ll be able to upload and download files from S3 buckets directly through Python code.

---

## Installation and Setup

### 1. Create an AWS Account
- Go to [AWS Console](https://aws.amazon.com/console/).
- Sign up for a free account (you’ll need a credit card, but you can use the free tier).
- Once signed in, create an **IAM User** (not the root account) for security.
  - Navigate to **IAM > Users > Add Users**.
  - Enable **Programmatic access**.
  - Assign permissions (for simplicity, you can start with `AmazonS3FullAccess`).

### 2. Install AWS CLI
Install the AWS Command Line Interface (CLI) on your system:

```bash
# macOS / Linux
brew install awscli

# Windows (via Chocolatey)
choco install awscli
```

### 3. Verify Installation

```bash
aws --version
```

### 4. Configure your AWS Account

```bash
aws configure
```

1. Make sure to get your access keys from the AWS console.

- You will be prompted for:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - REGION
    - OUTPUT_FORMAT

### 5. Install Python Modules

```bash
pip install boto3 pandas
```

### Basic Usage with S3 Client

1. Create a S3 Client

```python
import boto3

# Create an S3 client
s3 = boto3.client("s3")

# List buckets
response = s3.list_buckets()
print("Your Buckets:")
for bucket in response["Buckets"]:
    print(f"  {bucket['Name']}")
```

2. Upload a File to S3

```python
s3.upload_file("local_file.csv", "my-bucket", "uploads/local_file.csv")
print("Upload complete!")
```

3. Download a File from S3

```python
s3.download_file("my-bucket", "uploads/local_file.csv", "downloaded_file.csv")
print("Download complete!")
```