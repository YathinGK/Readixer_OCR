# Readixer_OCR

This project includes both a frontend built with React + Vite and a backend using Python + Streamlit to perform OCR (Optical Character Recognition) on handwritten documents using the Google Vision API.

## 🧠 Backend Features (Streamlit + Google Vision)
- Secure OCR processing with Google Cloud Vision
- Reads credentials from environment variable (`GCLOUD_CREDENTIALS_BASE64`)
- Generates clean PDF from extracted text
- Accepts uploaded handwritten images

## ⚛️ Frontend Features (React + Vite)
This frontend uses a minimal setup to get React working with Vite and Hot Module Reloading (HMR), plus some ESLint rules.

Currently, two official plugins are supported:
- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc)

If you're expanding the ESLint configuration for a production application, consider using TypeScript and `typescript-eslint`. See [this TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for integration guidance.

---

## 🚀 Deployment
Deployed securely on Render using environment variables (no credentials committed).

---

## 🔒 Security
The Google service account key is **never stored in the repo** and is loaded securely from an environment variable on the server.

---

## 📦 Tech Stack
- Streamlit (Python)
- Google Vision API
- React + Vite
- Node.js
