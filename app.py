import streamlit as st
import os
import speech_recognition as sr


from dotenv import load_dotenv
from groq import Groq


from utils.pdf_reader import extract_text
from utils.ocr_reader import extract_text_from_image
from utils.pdf_export import create_pdf
from utils.charts import create_chart
from utils.image_fetcher import get_exercise_image
from utils.voice_input import get_voice_input
from utils.translator import translate_text

from rag.dataset_loader import load_medical_dataset
from rag.embeddings import create_embeddings
from rag.vector_store import MedicalVectorStore
from rag.retriever import retrieve_context


# =========================
# Load Environment Variables
# =========================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =========================
# Build RAG Knowledge Base
# =========================

@st.cache_resource
def load_rag():

    documents = load_medical_dataset()

    embeddings = create_embeddings(documents)

    vector_store = MedicalVectorStore()

    vector_store.build(
        embeddings,
        documents
    )

    return vector_store


vector_store = load_rag()


# =========================
# Streamlit Config
# =========================

st.set_page_config(
    page_title="MediInsight AI",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 MediInsight AI")




if "report_text" not in st.session_state:
    st.session_state.report_text = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = ""

if "history" not in st.session_state:
    st.session_state.history = []

st.sidebar.header("📁 Previous Reports")

for i, item in enumerate(st.session_state.history):
    st.sidebar.write(f"Report {i+1}")

st.markdown("""
Upload a Medical Report and get:

✅ Report Summary

✅ Abnormal Findings

✅ Possible Conditions

✅ Diet Suggestions

✅ Lifestyle Suggestions

✅ Doctor Consultation Advice
""")


# =========================
# File Upload
# =========================

uploaded_file = st.file_uploader(
    "Upload Medical Report",
    type=["pdf", "png", "jpg", "jpeg", "webp"]
)

# =========================
# Compare Two Reports
# =========================

st.divider()

st.subheader("📊 Compare Two Reports")

compare_files = st.file_uploader(
    "Upload Two PDF Reports",
    type=["pdf"],
    accept_multiple_files=True,
    key="compare_reports"
)

if compare_files:

    if len(compare_files) != 2:
        st.warning("Please upload exactly 2 PDF reports.")

    else:

        if st.button("Compare Reports"):

            try:

                with st.spinner("Reading Reports..."):

                    report1 = extract_text(compare_files[0])
                    report2 = extract_text(compare_files[1])

                st.success("Reports Loaded Successfully")

                compare_prompt = f"""
You are an AI Healthcare Assistant.

Medical Report 1:

{report1}

Medical Report 2:

{report2}

Compare both reports and provide:

1. Improvements
2. Worsened Parameters
3. New Findings
4. Health Trend
5. Risk Assessment
6. Doctor Consultation Advice

Important Rules:
- Do NOT diagnose diseases.
- Do NOT prescribe medicines.
- Do NOT suggest treatments.
- Only provide educational health guidance.
- Use simple language.
"""

                with st.spinner("Comparing Reports..."):

                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {
                                "role": "user",
                                "content": compare_prompt
                            }
                        ],
                        temperature=0.3,
                        max_tokens=1500
                    )

                comparison_result = (
                    response
                    .choices[0]
                    .message
                    .content
                )

                st.subheader("📊 Comparison Result")
                st.write(comparison_result)

            except Exception as e:

                st.error(
                    f"Comparison Error: {str(e)}"
                )





# =========================
# Process File
# =========================

if uploaded_file:

    report_text = ""

    with st.spinner("Reading Report..."):

        file_name = uploaded_file.name.lower()

        # PDF
        if file_name.endswith(".pdf"):

            report_text = extract_text(
                uploaded_file
            )

        # Images
        else:

            os.makedirs(
                "uploads",
                exist_ok=True
            )

            save_path = os.path.join(
                "uploads",
                uploaded_file.name
            )

            with open(save_path, "wb") as f:
                f.write(
                    uploaded_file.getbuffer()
                )

            report_text = extract_text_from_image(
                save_path
            )

    st.subheader("📄 Extracted Report")

    st.text_area(
        "Report Content",
        report_text,
        height=300
    )

# =========================
# Analyze Button
# =========================

    if st.button("Analyze Report"):

        with st.spinner("Analyzing Report..."):

            context = retrieve_context(
                report_text,
                vector_store
           )

            prompt = f"""
You are an AI Healthcare Assistant.

Medical Knowledge Base:

{context}

Uploaded Medical Report:

{report_text}

Analyze the report and provide:

1. Report Summary

2. Abnormal Findings

3. Possible Conditions

4. Diet Recommendations

5. Lifestyle Recommendations

6. Whether doctor consultation is recommended

7. Risk Level (Low / Medium / High)

8. Reason for Risk Level

9. Recommended Specialist

Important Rules:

- Do NOT diagnose diseases.
- Do NOT prescribe medicines.
- Do NOT provide treatment.
- Only provide educational health guidance.
- Always include a disclaimer.
"""

        try:

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=1500
            )

            result = (
                response
                .choices[0]
                .message
                .content
            )

            st.session_state.report_text = report_text
            st.session_state.analysis_result = result
            st.session_state.history.append(result)

            st.subheader("🩺 AI Analysis")

            st.write(result)



            # =========================
            # Chart Section
            # =========================

            chart = create_chart()
            st.pyplot(chart)

            # =========================
            # PDF Download
            # =========================

            pdf_file = create_pdf(result)

            with open(pdf_file, "rb") as file:

                st.download_button(
                    label="📥 Download Analysis PDF",
                    data=file,
                    file_name="Medical_Analysis.pdf",
                    mime="application/pdf"
                )

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )


# =========================
# Translate Full Analysis
# =========================

if st.session_state.analysis_result:

    st.divider()

    st.subheader("🌍 Translate Full Report Analysis")

    languages = {
        "English": "en",
        "Hindi": "hi",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Punjabi": "pa",
        "Tamil": "ta",
        "Telugu": "te",
        "Bengali": "bn",
        "Urdu": "ur",
        "French": "fr",
        "Spanish": "es",
        "German": "de",
        "Arabic": "ar",
        "Chinese": "zh-CN",
        "Japanese": "ja"
    }

    selected_language = st.selectbox(
        "Select Language",
        list(languages.keys()),
        key="report_translation"
    )

    if st.button(
        "🌐 Translate Full Analysis",
        key="translate_full_report"
    ):

        translated_result = translate_text(
            st.session_state.analysis_result,
            languages[selected_language]
        )

        st.subheader("📖 Translated Report")

        st.write(translated_result)







# =========================
# Report Chatbot
# =========================

if st.session_state.analysis_result:

    st.divider()

    st.subheader("💬 Chat With Your Report")

    # Session State for Voice Input
    if "voice_question" not in st.session_state:
        st.session_state.voice_question = ""

    # Voice Button
    if st.button("🎤 Speak Question"):

        with st.spinner("Listening..."):

            st.session_state.voice_question = get_voice_input()

            st.success(
                f"You said: {st.session_state.voice_question}"
            )

    # Textbox
    user_question = st.text_input(
        "Ask a question about your report",
        value=st.session_state.voice_question
    )

    # Ask AI
    if user_question:

        try:

            chat_prompt = f"""
Uploaded Medical Report:

{st.session_state.report_text}

AI Analysis:

{st.session_state.analysis_result}

User Question:

{user_question}

Instructions:

- Answer only from the uploaded report.
- Explain medical terms simply.
- Do not prescribe medicines.
- If the report does not contain the answer, say so.
"""

            chat_response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": chat_prompt
                    }
                ],
                temperature=0.3
            )

            answer = (
                chat_response
                .choices[0]
                .message
                .content
            )

            st.markdown("### 🤖 Answer")
            st.write(answer)

        except Exception as e:

            st.error(
                f"Chat Error: {str(e)}"
            )


# =========================
# Disease Exercise Guide
# =========================

st.divider()

st.subheader("🏃 Disease Exercise Guide")

disease_name = st.text_input(
    "Enter Disease Name"
)

if st.button("Show Exercise Plan"):

    with st.spinner("Generating Exercise Plan..."):

        prompt = f"""
Disease: {disease_name}

Provide:

1. Best Yoga Poses
2. Best Exercises
3. Duration
4. Frequency
5. Benefits
6. Precautions

Format properly.

Do not recommend medicines.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        exercise_result = (
            response
            .choices[0]
            .message
            .content
        )

        st.markdown("### 🏃 Exercise & Yoga Plan")
        st.write(exercise_result)

        exercise_keywords = [
            "walking",
            "cycling",
            "yoga",
            "stretching",
            "swimming",
            "jogging",
            "strength training",
            "aerobics"
        ]

        for exercise in exercise_keywords:

            if exercise.lower() in exercise_result.lower():

                image_url = get_exercise_image(
                    f"{exercise} exercise"
                )

                if image_url:

                    st.image(
                        image_url,
                        caption=exercise.title(),
                        width=500
                    )