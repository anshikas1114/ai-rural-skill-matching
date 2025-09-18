from flask import Flask, render_template, request
from matching import load_jobs, match_jobs
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


app = Flask(
    __name__,
    template_folder = os.path.join(BASE_DIR,'frontend','templates'),
     static_folder=os.path.join(BASE_DIR,'frontend','static') 
     )

# Load job dataset once at startup
jobs_data = load_jobs(os.path.join('backend','Jobs.json'))

@app.route('/')
def index():
    """Render homepage with input form"""
    return render_template("index.html")

@app.route('/match', methods=['POST'])
def match():
    """Process user input and show job matches"""
    user_skills = request.form.get("skills", "")
    if not user_skills.strip():
        return render_template("index.html", error="Please enter at least one skill.")

    matches = match_jobs(user_skills, jobs_data)
    return render_template("index.html", matches = matches,user_skills = user_skills)
    
if __name__ == '__main__':
    app.run(debug=True)

