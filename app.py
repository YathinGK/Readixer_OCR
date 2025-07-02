from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import os
import json
import cv2
import numpy as np
from google.cloud import vision
from google.oauth2 import service_account
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_JUSTIFY
from datetime import datetime

# === Summarizer import ===
from summarizer import extract_text_from_pdf, extractive_summary, save_summary_as_pdf

app = Flask(__name__)
CORS(app)

# === Google Vision API: Secure credentials from environment ===
creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if creds_json:
    creds_dict = json.loads(creds_json)
    client = vision.ImageAnnotatorClient(
        credentials=service_account.Credentials.from_service_account_info(creds_dict)
    )
else:
    raise EnvironmentError("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable")

# === Handwriting Conversion ===
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

        os.remove(preprocessed_path)
        os.remove(input_path)

        return send_file("handwritten_output.pdf", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# === Document Summarization ===
@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        file = request.files["file"]
        topic = request.form.get("topic")  # Get topic if provided
        input_path = "temp_input.pdf"
        file.save(input_path)

        text = extract_text_from_pdf(input_path)
        summary = extractive_summary(text, max_sentences=7, topic=topic)
        output_path = "summary_" + os.path.splitext(file.filename)[0] + ".pdf"
        final_path = save_summary_as_pdf(summary, output_path)

        os.remove(input_path)
        return send_file(final_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
