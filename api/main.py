from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import os

app = FastAPI()

# Allowing CORS for local testing
origins = [
    "http://192.168.160.129:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate-qr/")
async def generate_qr(url: str):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR Code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Replace special characters in URL for filename safety
    safe_url = url.replace('http://', '').replace('https://', '').replace('/', '-').replace('.', '-')

    directory = 'qrcodes'
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, f"{safe_url}.png")
    img.save(file_path)

    return {"qr_code_url": file_path}
