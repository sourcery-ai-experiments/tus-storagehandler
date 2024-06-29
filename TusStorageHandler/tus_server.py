"""TusServer Module defines the TusServer class for handling files."""

import os

from minio.error import S3Error


class TusServer:
  """Initializes a new instance of the TusServer class.

  Args:
      minio_client (Minio): The Minio client object used for file operations.
      bucket_name (str): The name of the Minio bucket to operate on.
  """

  def __init__(self, minio_client, bucket_name):
    """Initializes a new instance of the TusServer class.

    Args:
        minio_client (Minio): The Minio client object used for file operations.
        bucket_name (str): The name of the Minio bucket to operate on.

    """
    self.minio_client = minio_client
    self.bucket_name = bucket_name

  def get_file_path(self, upload_id):
    """Returns the file path for the given upload_id within the 'uploads' directory.

    Args:
        upload_id (str): Unique identifier for the upload.

    Returns:
        str: File path within the 'uploads' directory corresponding to the upload_id.

    """
    return os.path.join("uploads", upload_id)

  def write_file(self, upload_id, file_content):
    """Writes content to a file located at the specified upload_id location.

    Args:
        upload_id (str): Unique identifier for the upload location.
        file_content (bytes): Content to be written to the file.

    Raises:
        IOError: If there is an error writing to the file.

    """
    file_path = self.get_file_path(upload_id)
    if not os.path.exists(file_path):
      os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
      f.write(file_content)

  def assemble_file(self, upload_id, filename):
    """Uploads a file to Minio storage after assembling it from a temporary location.

    Args:
        upload_id (str): Unique identifier for the upload.
        filename (str): Name to assign to the uploaded file in Minio.

    Raises:
        Exception: If the file cannot be uploaded to Minio or if the file specified
                   by `upload_id` does not exist.

    """
    file_path = self.get_file_path(upload_id)
    if os.path.exists(file_path):
      try:
        # Upload the file to Minio
        self.minio_client.fput_object(self.bucket_name, filename, file_path)
      except S3Error as err:
        print(f"Failed to upload file to Minio: {err}")
        raise Exception("Failed to upload file to Minio") from err
      finally:
        # Remove the temporary file
        os.remove(file_path)
    else:
      raise Exception(f"File not found for upload_id: {upload_id}")
