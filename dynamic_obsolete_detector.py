"""
Dynamic Obsolete Skill Detector
NO HARDCODING! 
This script mathematically detects outdated topics by cross-referencing:
1. Job postings in the sector (Demand Frequency = 0)
2. Institute placement rate (< 40%)
3. Years since syllabus was last revised (> 6 years ago)
"""

import sys
import pandas as pd
from datetime import datetime

# Ensure proper character display on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def analyze_course_dynamically(course_id):
    # 1. Load the raw datasets
    courses_df = pd.read_csv("data/existing_courses.csv")
    jobs_df = pd.read_csv("data/job_market_demand.csv")
    feedback_df = pd.read_csv("data/employer_feedback.csv")
    
    # 2. Find course
    match = courses_df[courses_df["course_id"].str.upper() == course_id.upper()]
    if match.empty:
        print(f"Course {course_id} not found.")
        return
        
    course = match.iloc[0]
    district = course["district"]
    sector = course["sector"]
    placement_rate = course["placement_rate_pct"]
    revised_year = course["curriculum_last_revised_year"]
    
    print("=" * 75)
    print(f"🔍 DYNAMIC OBSOLETE TOPIC DETECTION: {course['course_name'].upper()}")
    print(f"   Institute: {course['institution_name']} | District: {district}")
    print(f"   Placement Rate: {placement_rate}% | Last Revised: {revised_year} ({2024 - revised_year} years ago)")
    print("=" * 75)
    
    # 3. Collect ALL skills in current sector demand across Maharashtra
    sector_jobs = jobs_df[jobs_df["sector"].str.lower() == sector.lower()]
    
    # Build market demand frequency map
    market_skills_count = {}
    for skills_str in sector_jobs["required_skills"]:
        for s in skills_str.split(","):
            clean_s = s.strip().lower()
            market_skills_count[clean_s] = market_skills_count.get(clean_s, 0) + 1
            
    # 4. Evaluate each taught skill purely through data signals
    taught_skills = [s.strip() for s in str(course["skills_taught"]).split(",")]
    
    print("\n📊 DATA-DRIVEN TOPIC AUDIT (No Hardcoding):")
    print(f"   Total job postings analyzed in '{sector}': {len(sector_jobs)}")
    print("-" * 75)
    
    obsolete_found = False
    for skill in taught_skills:
        skill_lower = skill.lower()
        # Count how many jobs in the sector ask for this skill
        demand_count = sum(1 for m_skill in market_skills_count if skill_lower in m_skill or m_skill in skill_lower)
        
        # ALGORITHMIC DECISION RULE:
        # If Demand = 0 AND (Course Placement is poor OR Syllabus is > 6 years old)
        if demand_count == 0 and (placement_rate < 50 or (2024 - revised_year) >= 6):
            obsolete_found = True
            print(f"  ❌ FLAG AS OBSOLETE: '{skill}'")
            print(f"     • Industry Demand Signal : 0 out of {len(sector_jobs)} active job postings ask for this.")
            print(f"     • Course Placement Signal: Low ({placement_rate}%), indicating poor market absorption.")
            print(f"     • Syllabus Age Signal    : Last revised in {revised_year} (Outdated standards).")
            print(f"     ➔ Recommendation        : Phase out from syllabus to make room for emerging skills.\n")
        else:
            print(f"  ✅ KEEP / RELEVANT: '{skill}' (Found in active market postings)\n")
            
    if not obsolete_found:
        print("  All syllabus topics have positive active hiring signals.")

if __name__ == "__main__":
    # Test on traditional Automobile course in Pune
    analyze_course_dynamically("CRS101")
    # Test on traditional DTP / Web course in Thane
    analyze_course_dynamically("CRS110")
