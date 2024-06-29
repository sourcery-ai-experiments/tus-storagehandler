# TUS Storage Handler

## Synopsis
This Flask application provides endpoints for uploading, downloading, and listing files in a MinIO bucket, with TUS protocol support for uploads, and CORS enabled for cross-origin requests.

## Installation

### Prerequisites
This flask application requires a running instance of [minio](https://min.io/download)

Run the minio instance by executing the following command in the location where minio is installed

`minio server /data --console-address ":9001"`

Download the required dependencies

1. Navigate to the folder `TusStorageHandler`
2. Create a virtual environment and activate it (optional)
3. `pip install -r requirements.txt`

### Running the application

`flask run`
The application will be running on `http://127.0.0.1:5000` by default.
