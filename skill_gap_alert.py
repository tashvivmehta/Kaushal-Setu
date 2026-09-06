"""
Feature: Skill Gap Alert
Finds skills that local companies are desperately hiring for,
but NO local college or ITI in that district is teaching!
"""

import sys
import pandas as pd

# Ensure proper character display on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def find_skill_gap_alerts(district_name):
    # 1. Load data
    jobs_df = pd.read_csv("data/job_market_demand.csv")
    courses_df = pd.read_csv("data/existing_courses.csv")
    
    # 2. Filter for the selected district
    district_jobs = jobs_df[jobs_df["district"].str.lower() == district_name.lower()]
    district_courses = courses_df[courses_df["district"].str.lower() == district_name.lower()]
    
    if district_jobs.empty:
        print(f"No job data found for district: {district_name}")
        return

    # 3. Collect ALL skills taught in local courses
    taught_skills = set()
    for skills_string in district_courses["skills_taught"].dropna():
        # Split "Skill1, Skill2, Skill3" by comma and strip extra spaces
        for s in skills_string.split(","):
            taught_skills.add(s.strip().lower())
            
    # 4. Check each job's required skills against taught skills
    print("=" * 70)
    print(f"🚨 SKILL GAP ALERTS FOR DISTRICT: {district_name.upper()}")
    print("   (High Demand Industry Skills Taught in 0 Local ITIs/Courses)")
    print("=" * 70)
    
    gap_count = 0
    for _, job in district_jobs.iterrows():
        job_skills = [s.strip() for s in job["required_skills"].split(",")]
        
        # Find which of these skills are NOT taught in any local course
        missing_skills = []
        for s in job_skills:
            if s.lower() not in taught_skills:
                missing_skills.append(s)
                
        if missing_skills:
            gap_count += 1
            print(f"🔴 ROLE IN DEMAND: {job['job_title']} ({job['industrial_cluster']})")
            print(f"   Open Vacancies : {job['open_vacancies']} openings | Avg Salary: Rs. {job['avg_monthly_salary_inr']}/mo")
            print(f"   Missing Skills : {', '.join(missing_skills)}")
            print(f"   Taught Locally : 0 local courses teach these skills!\n")
            
    if gap_count == 0:
        print("Great news! All required skills are currently covered by local courses.")

# Test the function for Pune and Chhatrapati Sambhajinagar
if __name__ == "__main__":
    find_skill_gap_alerts("Pune")
    find_skill_gap_alerts("Chhatrapati Sambhajinagar")
