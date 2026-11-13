from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image
import pytesseract
import io

app = FastAPI()

@app.get("/")
def home():
    return {"status": "OCR API running"}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    data = await file.read(5 * 1024 * 1024 + 1)

    if len(data) > 5 * 1024 * 1024:
        raise HTTPException(413, "File too large")

    try:
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            if image.width * image.height > 12_000_000:
                raise HTTPException(413, "Image dimensions too large")

            text = pytesseract.image_to_string(
                image.convert("RGB"),
                timeout=30
            )
        return {"text": text}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(400, "Invalid image or OCR failed")
