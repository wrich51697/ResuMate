from flask import render_template, request, jsonify
import os
import spacy
from werkzeug.utils import secure_filename
from collections import defaultdict

# Load the pre-trained spaCy model
nlp = spacy.load('en_core_web_sm')


# Function to extract skills from resume text
def extract_skills(resume_text):
    skillset = set()
    skills = ['Python', 'Machine Learning', 'SQL', 'Project Management']
    for skill in skills:
        if skill.lower() in resume_text.lower():
            skillset.add(skill)
    return skillset


# Function to parse resume using spaCy and extract entities
def parse_resume(resume_text):
    doc = nlp(resume_text)
    parsed_resume = defaultdict(str)
    for ent in doc.ents:
        parsed_resume[ent.label_] += ent.text + ' '
    return parsed_resume


def init_routes(app):
    @app.route('/')
    def index():
        print("Current working directory:", os.getcwd())
        return render_template('upload.html')


    @app.route('/upload', methods=['POST'])
    def upload_resume():
        if 'resume' not in request.files:
            return 'No file part'
        file = request.files['resume']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            with open(file_path, 'r') as f:
                resume_text = f.read()
            skills = extract_skills(resume_text)
            parsed_resume = parse_resume(resume_text)
            return jsonify({
                'skills': list(skills),
                'parsed_resume': dict(parsed_resume)
            })
