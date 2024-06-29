"""This module handles the loading of environment variables for MinIO configuration.

Environment variables expected:
- MINIO_HOSTNAME: The hostname for the MinIO server.
- MINIO_PORT: The port for the MinIO server.
- MINIO_ACCESS_KEY: The access key for MinIO.
- MINIO_SECRET_KEY: The secret key for MinIO.
- MINIO_IS_SECURE: Boolean to determine if the connection is secure.
- MINIO_BUCKET_NAME: The name of the bucket in MinIO.
"""

import os

from dotenv import load_dotenv

load_dotenv()

MINIO_HOSTNAME = os.getenv("MINIO_HOSTNAME")
MINIO_PORT = os.getenv("MINIO_PORT")
MINIO_ENDPOINT = f"{MINIO_HOSTNAME}:{MINIO_PORT}"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_IS_SECURE = os.getenv("MINIO_IS_SECURE", "true").lower() in ["true"]
MINIO_BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME")
