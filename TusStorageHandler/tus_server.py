import os
from minio.error import S3Error


class TusServer:
  def __init__(self, minio_client, bucket_name):
    self.minio_client = minio_client
    self.bucket_name = bucket_name

  def get_file_path(self, upload_id):
    return os.path.join("uploads", upload_id)

  def write_file(self, upload_id, file_content):
    file_path = self.get_file_path(upload_id)
    if not os.path.exists(file_path):
      os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as f:
      f.write(file_content)

  def assemble_file(self, upload_id, filename):
    file_path = self.get_file_path(upload_id)
    if os.path.exists(file_path):
      try:
        # Upload the file to Minio
        self.minio_client.fput_object(self.bucket_name, filename, file_path)
      except S3Error as err:
        print(err)
        raise Exception("Failed to upload file")
      finally:
        # Remove the temporary file
        os.remove(file_path)
    else:
      raise Exception(f"File not found for upload_id: {upload_id}")
