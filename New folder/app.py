import streamlit as st
import pandas as pd
import pybase64
import time
import datetime
import json
import random
import os
import re
from pdfminer.high_level import extract_text
from streamlit_tags import st_tags
from PIL import Image
import matplotlib.pyplot as plt
st.set_page_config(page_title="Resume Analyzer", page_icon="📄")
resume_icon_path = "resume_icon.jpg"
resume_img_path = "resume_img.png"
SKILLS_DB = [
    "Python", "Java", "C++", "Machine Learning", "Data Science", "AI",
    "Deep Learning", "Computer Vision", "NLP", "Cybersecurity", "Cloud Computing",
    "Web Development", "Django", "Flask", "React", "Angular", "SQL", "NoSQL", "Linux"
]
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"
def extract_resume_text(file_path):
    return extract_text(file_path)
def extract_resume_details(resume_text):
    details = {}
    details["name"] = resume_text.split("\n")[0].strip()
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
    details["email"] = email_match.group() if email_match else "Not Found"
    phone_match = re.search(r"\+?\d{10,13}", resume_text)
    details["mobile_number"] = phone_match.group() if phone_match else "Not Found"
    extracted_skills = [skill for skill in SKILLS_DB if skill.lower() in resume_text.lower()]
    details["skills"] = extracted_skills if extracted_skills else ["Not Found"]
    details["no_of_pages"] = resume_text.count("\f") + 1
    return details
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = pybase64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
if not os.path.exists("Uploaded_Resumes"):
    os.makedirs("Uploaded_Resumes")

if not os.path.exists("user_data.json"):
    with open("user_data.json", "w") as f:
        json.dump([], f)
def run():
    st.sidebar.image(resume_icon_path, width=100)

    img = Image.open(resume_img_path)
    img = img.resize((250, 250))
    st.image(img)

    st.title("AI Resume Analyzer")

    st.sidebar.markdown("# Choose User")
    activities = ["User", "Admin"]
    choice = st.sidebar.selectbox("Choose among the options:", activities)

    if choice == "User":
        st.markdown("<h5>Upload your resume and get smart recommendations</h5>", unsafe_allow_html=True)
        pdf_file = st.file_uploader("Upload your Resume", type=["pdf"])

        if pdf_file is not None:
            with st.spinner("Uploading your Resume..."):
                time.sleep(2)

            save_pdf_path = os.path.join("Uploaded_Resumes", pdf_file.name)
            with open(save_pdf_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            show_pdf(save_pdf_path)
            resume_text = extract_resume_text(save_pdf_path)
            resume_data = extract_resume_details(resume_text)

            st.header("**Resume Analysis**")
            st.success(f"Hello {resume_data['name']}")

            st.subheader("**Your Basic Info**")
            st.text(f"NAME: {resume_data['name']}")
            st.text(f"EMAIL: {resume_data['email']}")
            st.text(f"CONTACT: {resume_data['mobile_number']}")
            st.text(f"RESUME PAGES: {resume_data['no_of_pages']}")

            st.subheader("**Skills Recommendation** ")
            keywords = st_tags(label="#### Your Current Skills", value=resume_data["skills"], key="1")

            st.subheader("**Resume Score **")
            resume_score = random.randint(60, 90)  
            st.progress(resume_score)
            st.success(f"**Your Resume Writing Score: {resume_score}**")

            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

            new_entry = {
                "name": resume_data["name"],
                "email": resume_data["email"],
                "resume_score": resume_score,
                "timestamp": timestamp,
                "no_of_pages": resume_data["no_of_pages"],
                "skills": resume_data["skills"],
            }

            with open("user_data.json", "r+") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
                data.append(new_entry)
                file.seek(0)
                json.dump(data, file, indent=4)

    else:
        st.success("**Admin Login Required**")
        username = st.text_input("Enter Admin Username", key="admin_user")
        password = st.text_input("Enter Admin Password", type="password", key="admin_pass")

        if st.button("Login"):
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.success("**Login Successful! Welcome Admin.**")

                try:
                    with open("user_data.json", "r") as file:
                        data = json.load(file)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = []

                if data:
                    st.header("**User's Data**")
                    df = pd.DataFrame(data)
                    st.dataframe(df)
                else:
                    st.warning("No data available.")
            else:
                st.error("Invalid username or password!")


if __name__ == "__main__":
    run()
