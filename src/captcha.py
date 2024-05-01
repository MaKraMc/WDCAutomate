from PIL import Image
from io import BytesIO
import pytesseract

def solveCaptcha(captchaImage):
    #[DEBUG]Save the captcha image
    #with open("./captcha.png", "wb") as f:
    #    f.write(captchaImage)

    # Solve the captcha
    # First, convert the image to bytes
    captchaImageBytes = Image.open(BytesIO(captchaImage))
    # Then we can open the image with pytesseract ocr
    captchaSolution = pytesseract.image_to_string(captchaImageBytes, config='--dpi 100').strip()
    print(f"Got captcha: {captchaSolution}")

    return captchaSolution