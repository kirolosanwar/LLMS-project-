import os
import json
import PyPDF2
import traceback
import re
import ast

def read_file(file):
    filename = file.name.lower()
    if filename.endswith(".pdf"):  
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise Exception("Error Reading The PDF File") from e
    elif filename.endswith(".txt"):  
        return file.read().decode("utf-8")
    else:
        raise Exception(
            "Unsupported file format. Only PDF and TXT files are supported."
        )

def get_table_data(quiz_str):
    try:
        # 🟢 استخراج أول كتلة JSON
        match = re.search(r"\{.*\}", quiz_str, re.DOTALL)
        if not match:
            raise ValueError("No JSON object found in quiz_str")

        clean_str = match.group()

        # 🟢 أولوية 1: تجربة json.loads
        try:
            quiz_dict = json.loads(clean_str)
        except json.JSONDecodeError:
            # 🟢 أولوية 2: تجربة ast.literal_eval (يتحمل أخطاء بسيطة)
            quiz_dict = ast.literal_eval(clean_str)

        quiz_table_data = []
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = ' || '.join(
                f"{option} {option_value}" for option, option_value in value["options"].items()
            )
            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "choices": options, "Correct": correct})

        return quiz_table_data

    except Exception as e:
        print("⚠️ RAW QUIZ OUTPUT:", quiz_str[:500])  # Debug
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
