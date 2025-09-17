import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqgenerator.MCQgenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

# ================= تحميل الـ API KEY =================
load_dotenv()

# ================= تحميل ملف JSON =================
with open(r"C:\Users\LAP-STORE\Desktop\Amit\langchain\Q&A_project\Response.json", "r") as file:
    RESPONSE_JSON = json.load(file)

# ================= واجهة Streamlit =================
st.title("MCQs Creator Application")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or text file")

    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity level of questions", max_chars=20, placeholder="Simple")

    button = st.form_submit_button("Create MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating MCQs..."):
            try:
                # قراءة النص من الملف
                text = read_file(uploaded_file)

                # ✅ استدعاء السلسلة الرئيسية (توليد + تقييم) باستخدام dict
                response = generate_evaluate_chain({
                    "text": text,
                    "number": mcq_count,
                    "subject": subject,
                    "tone": tone,
                    "response_json": RESPONSE_JSON,
                })

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("❌ Error while generating MCQs")
            else:
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    review = response.get("review", "")

                    if quiz:
                        table_data = get_table_data(quiz)
                        if table_data:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)

                            # عرض التقييم
                            st.text_area(label="Review", value=review)
                        else:
                            st.error("⚠️ Error in table data formatting")
                else:
                    st.write(response)
