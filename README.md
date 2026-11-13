# Tesseract OCR API

A free, open-source OCR REST API built with **Tesseract OCR, Python, and FastAPI**.

This project extracts text from images and returns the recognized text in JSON format.

## Features

- Extract text from JPG and PNG images
- Free and open-source OCR engine
- REST API using FastAPI
- Automatic API documentation
- Docker support
- No paid OCR API required
- English text recognition

## Technologies

- **Python 3.11** — Backend language
- **FastAPI** — REST API framework
- **Tesseract OCR** — Text recognition engine
- **Pytesseract** — Python interface for Tesseract
- **Docker** — Application deployment

## API Endpoints

### GET /

Check whether the API is running.

Response:

```json
{
  "status": "OCR API running"
}
```

### POST /ocr

Upload an image to extract text.

**Supported formats:** JPG and PNG

**Maximum upload size:** 2 MB

**Maximum image dimensions:** 4 million pixels

Example response:

```json
{
  "text": "Hello, this is a test document."
}
```

## Deployment

The project includes a Dockerfile that installs Tesseract OCR and starts the FastAPI server.

The application can be deployed to a compatible Docker hosting provider.

## API Documentation

After deployment, visit:

`https://YOUR-APP-URL/docs`

FastAPI provides an interactive interface for testing the OCR endpoint.

## License

Tesseract OCR is licensed under Apache License 2.0. The license for this API project's own code has not yet been specified.

## Future Features

- Scanned PDF OCR
- Multiple language support
- Batch image processing
- Searchable PDF generation
- Integration with PDF conversion websites
