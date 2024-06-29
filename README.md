# Crypt4GH Middleware for proTES
[![license][badge-license]][badge-url-license]
[![chat][badge-chat]][badge-url-chat]

## Synopsis
This Flask application provides endpoints for uploading, downloading, and listing files in a MinIO bucket, with TUS protocol support for uploads and CORS enabled for cross-origin requests.

## Installation

### Prerequisites
This flask application requires a running instance of [minio](https://min.io/download)

Run the minio instance by executing the following command in the location where minio is installed

`minio server /data --console-address ":9001"`

Download the required dependencies

1. Navigate to the folder `TusStorageHandler`
2. Create a virtual environment and activate it (optional)
3. `pip install requirements.txt`

### Running the application

`flask run`
The application will be running on `http://127.0.0.1:5000` by default.

## Contributing

## Code of Conduct

## Versioning

## License

This project is distributed under the [Apache License 2.0][badge-license], a
copy of which is also available in [`LICENSE`][license].

## Contact

The project is maintained by [ELIXIR Cloud & AAI][elixir-cloud-aai], a Driver
Project of the [Global Alliance for Genomics and Health (GA4GH)][ga4gh], under
the umbrella of the [ELIXIR][elixir] [Compute Platform][elixir-compute].

- For filing bug reports, feature requests or other code-related issues, please
  make use of the project's [issue tracker](https://github.com/elixir-cloud-aai/tus-storagehandler/issues).