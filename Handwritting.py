import os
import base64
import cv2
import numpy as np
from google.cloud import vision
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

# 🔐 Load base64-encoded credentials from environment variable (used in GitHub deployment)
base64_creds = os.getenv("GCLOUD_CREDENTIALS_BASE64")
if base64_creds:
    with open("credentials.json", "wb") as f:
        f.write(base64.b64decode(base64_creds))
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
else:
    # Fallback for local development if not using GitHub Secrets
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "handwrittenpersonal-ee760a4396bf.json"

# ✅ Register Times New Roman font (requires times.ttf in directory)
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))  

def preprocess_image(image_path):
    """Preprocess the image to enhance OCR accuracy."""
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image at {image_path} not found.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    preprocessed_path = 'processed_note.png'
    cv2.imwrite(preprocessed_path, thresh)
    return preprocessed_path

def recognize_text(image_path):
    """Extract handwritten text from image using Google Cloud Vision."""
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")

    return response.full_text_annotation.text if response.full_text_annotation.text else "No text detected."

def generate_pdf(text, output_path='handwritten_output.pdf'):
    """Generate a justified PDF using ReportLab and Times New Roman font."""
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title',
        fontName='Times-Roman',
        fontSize=18,
        leading=22,
        alignment=1,  # Center
        spaceAfter=12
    )

    body_style = ParagraphStyle(
        name='Body',
        fontName='Times-Roman',
        fontSize=12,
        leading=16,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )

    content = []
    title = Paragraph("Handwritten Notes to Digital Text", title_style)
    content.append(title)
    content.append(Spacer(1, 0.2 * inch))

    date_str = datetime.now().strftime("%B %d, %Y")
    content.append(Paragraph(f"Generated on: {date_str}", body_style))
    content.append(Spacer(1, 0.2 * inch))

    for para in text.strip().split('\n'):
        if para.strip():
            content.append(Paragraph(para.strip(), body_style))

    doc.build(content)
    print(f"✅ PDF generated at: {output_path}")

def main():
    """Main function to handle image input, OCR processing, and PDF generation."""
    try:
        image_path = input("Enter the path to the handwritten note image (e.g., note.png): ").strip()
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"No such file: {image_path}")

        preprocessed_path = preprocess_image(image_path)
        print("🛠️ Image preprocessing complete...")

        text = recognize_text(preprocessed_path)
        print("\n📄 Extracted Text:\n", text)

        generate_pdf(text, 'handwritten_output.pdf')

        if os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
