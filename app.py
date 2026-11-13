
from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import (
    Image,
    ImageEnhance,
    ImageFilter,
    ImageOps,
    UnidentifiedImageError,
)
import pytesseract
import io

app = FastAPI()

MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_PIXELS = 12_000_000

@app.get("/")
def home():
    return {"status": "OCR API running"}

@app.post("/ocr")
async def ocr(file: UploadFile = File(...)):
    data = await file.read(MAX_FILE_SIZE + 1)

    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )

    try:
        with Image.open(io.BytesIO(data)) as image:

            if image.width * image.height > MAX_PIXELS:
                raise HTTPException(
                    status_code=413,
                    detail="Image dimensions too large"
                )

            image.load()

            # Convert image to grayscale
            processed = ImageOps.grayscale(image)

            # Enlarge small text (maximum 2x)
            if processed.width < 1600:
                scale = min(2, 2400 / processed.width)

                new_width = int(processed.width * scale)
                new_height = int(processed.height * scale)

                # Prevent excessive memory usage
                if new_width * new_height <= MAX_PIXELS:
                    processed = processed.resize(
                        (new_width, new_height),
                        Image.Resampling.LANCZOS
                    )

            # Enhance contrast
            processed = ImageEnhance.Contrast(
                processed
            ).enhance(1.5)

            # Sharpen text
            processed = processed.filter(
                ImageFilter.UnsharpMask(
                    radius=1,
                    percent=120,
                    threshold=2
                )
            )

            # Recognize text
            text = pytesseract.image_to_string(
                processed,
                config="--oem 1 --psm 3",
                timeout=30
            )

        return {
            "success": True,
            "text": text
        }

    except HTTPException:
        raise

    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(
            status_code=400,
            detail="Invalid image"
        )

    except pytesseract.TesseractError:
        raise HTTPException(
            status_code=500,
            detail="OCR engine error"
        )

    except RuntimeError:
        raise HTTPException(
            status_code=500,
            detail="OCR processing failed"
        )
