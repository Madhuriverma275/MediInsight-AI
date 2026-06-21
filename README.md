# 🏥 MediInsight AI

MediInsight AI is an AI-powered Medical Report Analysis System built using Streamlit, Groq LLM, OCR, and RAG (Retrieval-Augmented Generation).

The application helps users understand medical reports in a simple way by providing report summaries, abnormal findings, lifestyle suggestions, report comparison, multilingual translation, and an AI-powered healthcare chatbot.

---

# ✨ Features

## 📄 Medical Report Analysis

* Upload PDF medical reports
* Upload image reports (PNG, JPG, JPEG, WEBP)
* OCR-based text extraction
* AI-powered report analysis

## 🩺 Health Insights

* Report Summary
* Abnormal Findings
* Possible Conditions
* Diet Recommendations
* Lifestyle Recommendations
* Risk Assessment
* Specialist Recommendation

## 💬 AI Report Chatbot

* Ask questions about uploaded reports
* Context-aware responses
* Simple medical explanations

## 🎤 Voice Support

* Voice-based question input
* Speech-to-Text integration

## 📊 Report Comparison

* Compare two medical reports
* Identify improvements
* Detect worsened parameters
* Track health trends

## 📥 PDF Export

* Download AI analysis as PDF

## 🌍 Multilingual Translation

* Translate analysis into multiple languages
* Hindi
* Marathi
* Gujarati
* Punjabi
* Tamil
* Telugu
* Bengali
* Urdu
* French
* Spanish
* German
* Arabic
* Chinese
* Japanese

## 🏃 Exercise & Yoga Guide

* Disease-specific exercise recommendations
* Yoga recommendations
* Exercise images fetched from the internet

## 🧠 RAG-Based Medical Knowledge

* Medical knowledge retrieval
* Context-aware report analysis

---

# 🛠️ Tech Stack

* Python
* Streamlit
* Groq API
* EasyOCR
* FAISS
* Sentence Transformers
* Deep Translator
* Speech Recognition
* FPDF
* Matplotlib

---

# 📂 Project Structure

MediInsight_AI/

├── app.py

├── data/

├── rag/

│   ├── dataset_loader.py

│   ├── embeddings.py

│   ├── retriever.py

│   └── vector_store.py

├── utils/

│   ├── pdf_reader.py

│   ├── ocr_reader.py

│   ├── pdf_export.py

│   ├── charts.py

│   ├── voice_input.py

│   ├── image_fetcher.py

│   └── translator.py

├── screenshots/

├── requirements.txt

├── .env

└── README.md

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone YOUR_REPOSITORY_LINK
```

```bash
cd MediInsight_AI
```

---

## 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

---

## 3. Create .env File

Create a file named:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
PEXELS_API_KEY=your_pexels_api_key
```

---

## 4. Run Application

```bash
python -m streamlit run app.py
```

---

# 📸 Screenshots

Add screenshots inside:

```text
screenshots/
```

Recommended screenshots:

* Home 
* Analysis Report
* Chatbot
* Comparison Two Reports
* Translate
* Disease Exercise Guide
* Charts

---

# 🔒 Disclaimer

This project is intended for educational and informational purposes only.

* It does not diagnose diseases.
* It does not prescribe medicines.
* It does not provide medical treatment.
* Always consult a qualified healthcare professional for medical advice.

---

# 👨‍💻 Developer

Madhuri Verma

B.Tech Student | AI & Python Developer

---

# ⭐ Future Enhancements

* Doctor Finder
* Hospital Recommendation
* Medicine Information
* WhatsApp Integration
* Cloud Database
* User Authentication
* Health History Tracking
* Mobile Application
