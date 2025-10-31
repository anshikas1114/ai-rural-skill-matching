from flask import Flask, render_template, request, jsonify
from matching import load_jobs, match_jobs
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


app = Flask(
    __name__,
    template_folder = os.path.join(BASE_DIR,'frontend','templates'),
     static_folder=os.path.join(BASE_DIR,'frontend','static') 
     )

# Load job dataset once at startup
jobs_data = load_jobs(os.path.join(os.path.dirname(__file__), 'Jobs.json'))

@app.route('/')
def index():
    """Render homepage with input form"""
    return render_template("index.html")

@app.route('/match', methods=['POST'])
def match():
    """Process user skills and return job matches as JSON"""
    data = request.get_json()
    user_skills = data.get("skills", "")
    
    if not user_skills.strip():
        # Return a JSON error with a 400 Bad Request status code
        return jsonify({"error": "Please enter at least one skill."}), 400
    
    matches = match_jobs(user_skills, jobs_data)
    
    # Return matches as a JSON object
    return jsonify({"matches": matches})

if __name__ == '__main__':
    app.run(debug=True)

