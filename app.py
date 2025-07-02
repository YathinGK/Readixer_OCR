from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
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

app = Flask(__name__)
CORS(app)

# Set the path to your Google Vision API key JSON
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'handwrittenpersonal-ee760a4396bf.json'

# Register font (ensure 'times.ttf' is in your project folder)
pdfmetrics.registerFont(TTFont('Times-Roman', 'times.ttf'))

def preprocess_image(image_path):
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
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(f"Vision API error: {response.error.message}")
    return response.full_text_annotation.text if response.full_text_annotation.text else "No text detected."

def generate_pdf(text, output_path='handwritten_output.pdf'):
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name='Title', fontName='Times-Roman', fontSize=18, leading=22,
        alignment=1, spaceAfter=12
    )
    body_style = ParagraphStyle(
        name='Body', fontName='Times-Roman', fontSize=12, leading=16,
        alignment=TA_JUSTIFY, spaceAfter=12
    )
    content = []
    content.append(Paragraph("Handwritten Notes to Digital Text", title_style))
    content.append(Spacer(1, 0.2 * inch))
    date_str = datetime.now().strftime("%B %d, %Y")
    content.append(Paragraph(f"Generated on: {date_str}", body_style))
    content.append(Spacer(1, 0.2 * inch))
    for para in text.strip().split('\n'):
        if para.strip():
            content.append(Paragraph(para.strip(), body_style))
    doc.build(content)

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]
        input_path = "input_image.png"
        file.save(input_path)

        preprocessed_path = preprocess_image(input_path)
        text = recognize_text(preprocessed_path)
        generate_pdf(text)

        # Clean up
        if os.path.exists(preprocessed_path):
            os.remove(preprocessed_path)
        if os.path.exists(input_path):
            os.remove(input_path)

        return send_file("handwritten_output.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
