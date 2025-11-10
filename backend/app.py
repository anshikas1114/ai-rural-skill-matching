from flask import Flask, render_template, request, jsonify
import os
import json
from sentence_transformers import SentenceTransformer, util

# Base directories for project structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
    static_folder=os.path.join(BASE_DIR, 'frontend', 'static')
)

# ---------- LOAD JOB DATA ----------
def load_jobs(filepath):
    """Load jobs from a JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

jobs_data = load_jobs(os.path.join(os.path.dirname(__file__), 'Jobs.json'))

# ---------- AI MODEL INITIALIZATION ----------
print("🔹 Loading AI model... (This may take a few seconds)")
model = SentenceTransformer('all-MiniLM-L6-v2')
print("✅ Model loaded successfully!")

# ---------- AI MATCHING FUNCTION ----------
def ai_match_jobs(user_input, jobs_data, top_n=5):
    """
    Use semantic similarity to match user's skills with job roles.
    """
    # Encode user input
    user_embedding = model.encode(user_input, convert_to_tensor=True)

    job_scores = []
    for job_title, job_skills in jobs_data.items():
        job_text = " ".join(job_skills)  # combine all skills into one string
        job_embedding = model.encode(job_text, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(user_embedding, job_embedding).item()
        job_scores.append((job_title, similarity))

    # Sort jobs by similarity (descending order)
    job_scores.sort(key=lambda x: x[1], reverse=True)

    # Return top matches
    top_matches = [{"job": job, "score": round(score * 100, 2)} for job, score in job_scores[:top_n]]
    return top_matches

# ---------- ROUTES ----------
@app.route('/')
def index():
    """Render homepage"""
    return render_template("index.html")

@app.route('/match', methods=['POST'])
def match():
    """Process user skills and return AI-based job matches as JSON"""
    data = request.get_json()
    user_skills = data.get("skills", "")

    if not user_skills.strip():
        return jsonify({"error": "Please enter at least one skill."}), 400

    # Get AI-based matches
    matches = ai_match_jobs(user_skills, jobs_data)

    return jsonify({"matches": matches})

# ---------- RUN APP ----------
if __name__ == '__main__':
    app.run(debug=True)
