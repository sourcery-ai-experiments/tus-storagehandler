"""Main application module for handling MinIO storage and TUS protocol with Flask."""

import datetime
import os
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS
from minio.error import S3Error
from minio_client import minio_client
from tus_server import TusServer
from werkzeug.utils import secure_filename

MINIO_BUCKET = os.getenv("MINIO_BUCKET_NAME")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

tus_server = TusServer(minio_client, MINIO_BUCKET)

@app.route("/", methods=["GET"])
def home():
    """Endpoint to return a welcome message."""
    return jsonify({"message": "Welcome to the MinIO TUS server!"}), 200

@app.route("/download", methods=["GET"])
def download_bucket():
    """Endpoint to list all objects in the MinIO bucket.

    It uses pre-signed download links.
    """
    try:
        objects = minio_client.list_objects(MINIO_BUCKET, recursive=True)
        download_links = []
        for obj in objects:
            download_url = minio_client.presigned_get_object(
                MINIO_BUCKET, obj.object_name, expires=datetime.timedelta(seconds=3600)
            )
            download_links.append(download_url)

        return jsonify({"download_links": download_links}), 200

    except S3Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Endpoint to provide a pre-signed URL for downloading a specific file."""
    try:
        download_url = minio_client.presigned_get_object(
            MINIO_BUCKET,
            filename,
            expires=datetime.timedelta(seconds=3600),
            response_headers={
              "response-content-disposition": f'attachment; filename="{filename}"'
            },
        )
        return jsonify({"download_url": download_url}), 200

    except S3Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/list_files", methods=["GET"])
def list_files():
    """Endpoint to list all files in the MinIO bucket."""
    try:
        objects = minio_client.list_objects(MINIO_BUCKET)
        files = [obj.object_name for obj in objects]
        return jsonify({"files": files}), 200

    except S3Error as err:
        return jsonify({"error": str(err)}), 500

@app.route("/upload", methods=["POST"])
def upload_file():
    """Endpoint to handle file uploads using the TUS protocol."""
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_files = request.files.getlist("file")
    success_responses = []
    error_responses = []

    for uploaded_file in uploaded_files:
        if uploaded_file.filename == "":
            error_responses.append({"error": "Empty filename provided"})
            continue

        upload_id = str(uuid.uuid4())
        filename = secure_filename(uploaded_file.filename)
        file_content = uploaded_file.read()

        if file_content:
            tus_server.write_file(upload_id, file_content)
            tus_server.assemble_file(upload_id, filename)
            location = f"http://{request.host}/upload/{upload_id}"
            success_responses.append({"filename": filename, "location": location})
        else:
            error_responses.append({
                "filename": filename,
                "error": "No file content provided"}
            )

    if error_responses:
        return jsonify({"errors": error_responses}), 400
    else:
        return jsonify({"success": success_responses}), 201

if __name__ == "__main__":
    app.run(debug=False)