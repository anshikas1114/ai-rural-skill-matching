import os
import json

def load_jobs(file="Jobs.json"):
    """Load job dataset from JSON file"""
    # Use _file_ to get the directory of the current script, ensuring the path is correct
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, file)

    try: 
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {file_path} not found! Check your file path and name.")    
        # Return an empty dictionary if the file is not found, matching the expected data type
        return {} 

def match_jobs(user_skills, jobs_data, top_n=5):
    """
    Match user skills to jobs.
    user_skills: string like "weaving, stitching"
    jobs_data: a dictionary of job titles and skill lists (from Jobs.json)
    Returns: list of tuples (job_name, score)
    """
    # 1. Clean and process user skills (case-insensitive and no extra spaces)
    user_skills_set = set(s.strip().lower() for s in user_skills.split(","))

    results = []
    # 2. CRITICAL FIX: Iterate over key-value pairs (job_name, skills_list) of the dictionary
    for job_name, skills_list in jobs_data.items(): 
        
        # 3. Process job skills for comparison (case-insensitive)
        job_skills_set = set(s.lower() for s in skills_list)
        
        # 4. Calculate score: Count the number of intersecting skills
        # This checks how many skills the user has are also required by the job
        score = len(user_skills_set.intersection(job_skills_set))
        
        if score > 0:
            results.append((job_name, score))

    # Sort by best match (highest score first)
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]

# Test the function directly (only runs when the script is executed directly)
if __name__ == "_main_":
    jobs_data = load_jobs()
    if not jobs_data:
        print("Cannot run test, job data is empty.")
    else:
        test_skills = input('Enter the skills (comma separated): ')
        matches = match_jobs(test_skills, jobs_data)
        print("\n--- Matching Results ---")
        print("User Skills:", test_skills)
        if matches:
            print("Matched Jobs:")
            for job, score in matches:
                print(f"- {job} (Score: {score})")
        else:
            print("No jobs found for the given skills.")