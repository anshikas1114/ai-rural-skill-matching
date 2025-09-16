from flask import Flask, request, jsonify, render_template
import json
from matching import find_matching_jobs  # function from matching.py

app = Flask(__name__)

# Load jobs from JSON file
with open("jobs.json", "r") as f:
    jobs = json.load(f)

# Route for homepage
@app.route("/")
def home():
    return render_template("index.html")  # Make sure templates/index.html exists

# Route for matching skills
@app.route("/match", methods=["POST"])
def match():
    data = request.get_json()
    user_skills = data.get("skills", [])

    if not user_skills:
        return jsonify({"error": "No skills provided"}), 400

    matches = find_matching_jobs(user_skills, jobs)

    return jsonify({"matches": matches})

if __name__ == "__main__":
    app.run(debug=True)
