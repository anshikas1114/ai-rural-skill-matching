import os
import json

def load_jobs(file ="Jobs.json"):
    """Load job dataset from JSON file"""
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir,file) 

    try : 
     with open(file, "r", encoding="utf-8") as f:
        return json.load(f)
    except FileNotFoundError:
       print("Error: file path not found!")    
       return{}    

def match_jobs(user_skills, jobs_data, top_n=5):
    """
    Match user skills to jobs.
    user_skills: string like "weaving, stitching"
    jobs_data: dictionary from jobs.json
    Returns: list of tuples (job, score)
    """
    # Clean and split user skills
    user_skills = [s.strip().lower() for s in user_skills.split(",")]

    results = []
    for job, skills in jobs_data.items():
        # Count how many skills match
        score = len(set(user_skills) & set([s.lower() for s in skills]))
        if score > 0:
            results.append((job, score))

    # Sort by best match
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]

# Test the function directly
if __name__ == "__main__":
    jobs_data = load_jobs()
    test_skills = input('Enter the skills: ')
    matches = match_jobs(test_skills, jobs_data)
    print("User Skills:", test_skills)
    print("Matched Jobs:", matches)

