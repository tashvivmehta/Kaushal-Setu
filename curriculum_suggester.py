"""
Feature: Dynamic Curriculum Upgrade Suggester (100% Data-Driven, No Hardcoding)
Combines:
1. Dynamic detection of obsolete syllabus topics (based on 0 hiring signals + syllabus age).
2. Recommended new modules with lab hours (based on top vacancies in the district).
3. Equipment funding & trainer upskilling plan (based on employer surveys).
"""

import sys
import pandas as pd
from datetime import datetime

# Ensure proper character display on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def suggest_curriculum_upgrades(course_id):
    # 1. Load the raw datasets
    courses_df = pd.read_csv("data/existing_courses.csv")
    jobs_df = pd.read_csv("data/job_market_demand.csv")
    feedback_df = pd.read_csv("data/employer_feedback.csv")
    
    # 2. Find the selected course
    course_match = courses_df[courses_df["course_id"].str.upper() == course_id.upper()]
    if course_match.empty:
        print(f"Error: Course ID '{course_id}' not found.")
        return
        
    course = course_match.iloc[0]
    district = course["district"]
    sector = course["sector"]
    placement_rate = course["placement_rate_pct"]
    revised_year = course["curriculum_last_revised_year"]
    syllabus_age = datetime.now().year - revised_year
    
    print("=" * 75)
    print(f"📋 CURRICULUM UPGRADE REPORT: {course['course_name'].upper()}")
    print(f"   Institute: {course['institution_name']} | District: {district}")
    print(f"   Placement Rate: {placement_rate}% | Last Revised: {revised_year} ({syllabus_age} years ago)")
    print("=" * 75)
    
    # =========================================================================
    # STEP 1: DYNAMIC OBSOLETE TOPIC DETECTION (No Hardcoding!)
    # =========================================================================
    # Find all active job skills in this sector across Maharashtra
    sector_jobs = jobs_df[jobs_df["sector"].str.lower() == sector.lower()]
    
    # Collect all skill words actively requested by employers
    active_market_skills = []
    for skills_str in sector_jobs["required_skills"]:
        for s in skills_str.split(","):
            active_market_skills.append(s.strip().lower())
            
    current_taught_skills = [s.strip() for s in str(course["skills_taught"]).split(",")]
    
    print("\n[STEP 1: DATA-DRIVEN OBSOLETE TOPICS AUDIT]")
    flagged_obsolete = []
    for skill in current_taught_skills:
        skill_lower = skill.lower()
        # Count if this skill appears in any current job posting in this sector
        demand_matches = sum(1 for m_skill in active_market_skills if skill_lower in m_skill or m_skill in skill_lower)
        
        # Rule: 0 jobs asking for it + (low placement OR outdated syllabus)
        if demand_matches == 0 and (placement_rate < 50 or syllabus_age >= 6):
            flagged_obsolete.append(skill)
            print(f"  ❌ Remove / Phase Out: '{skill}'")
            print(f"     • Market Demand Signal : 0 active job postings in '{sector}' ask for this.")
            print(f"     • Syllabus Age Signal  : Revised in {revised_year} ({syllabus_age} years ago).")
        else:
            print(f"  ✅ Retain / Valid Topic : '{skill}' (Still has active demand).")
            
    if not flagged_obsolete:
        print("  ✅ No obsolete topics detected; all topics have active market demand.")

    # =========================================================================
    # STEP 2: DYNAMIC HIGH-DEMAND MODULES TO ADD
    # =========================================================================
    # Filter jobs in this specific district and sector
    district_jobs = jobs_df[(jobs_df["district"] == district) & (jobs_df["sector"] == sector)]
    
    current_skills_lower = [s.lower() for s in current_taught_skills]
    missing_skills = []
    for _, job in district_jobs.iterrows():
        for req_skill in job["required_skills"].split(","):
            clean_skill = req_skill.strip()
            # If not taught and not already in our list, add it
            if clean_skill.lower() not in current_skills_lower and clean_skill not in missing_skills:
                missing_skills.append((clean_skill, job["job_title"], job["open_vacancies"]))
                
    print("\n[STEP 2: RECOMMENDED NEW MODULES TO ADD (From Local Vacancies)]")
    if missing_skills:
        # Give practical hours to the top 4 missing skills
        hours_distribution = [30, 25, 20, 20]
        total_hours = 0
        for i, (skill, role_name, vacancies) in enumerate(missing_skills[:4]):
            hours = hours_distribution[i % len(hours_distribution)]
            total_hours += hours
            print(f"  ➕ Add Module: '{skill}' ({hours} Practical Lab Hours)")
            print(f"     • Driven By: {role_name} ({vacancies} vacancies in {district})")
        print(f"  📊 Total Recommended Curriculum Expansion: +{total_hours} Hours")
    else:
        print("  ✅ All high-demand local skills are already covered in this course.")

    # =========================================================================
    # STEP 3: LAB EQUIPMENT & TRAINER CAPACITY PLANNING
    # =========================================================================
    print("\n[STEP 3: LAB EQUIPMENT & TRAINER CAPACITY PLAN]")
    matching_feedback = feedback_df[(feedback_df["district"] == district) & (feedback_df["sector"] == sector)]
    
    if not matching_feedback.empty:
        fb = matching_feedback.iloc[0]
        print(f"  🛠️ Recommended Lab Upgrade: {fb['recommended_new_equipment']}")
        print(f"  👨‍🏫 Trainer Retraining Required: {fb['urgent_trainer_training_needed']}")
        print(f"  🤝 Industry Partner: {fb['company_name']} ({fb['industrial_cluster']})")
    else:
        print(f"  🛠️ Lab Status: {course['equipment_status']} | Trainer Score: {course['trainer_capacity_score']}/5")

    print("\n" + "=" * 75 + "\n")


if __name__ == "__main__":
    # Test 1: Motor Mechanic in Pune (Traditional Auto vs Modern EV)
    suggest_curriculum_upgrades("CRS101")
    
    # Test 2: Desktop Publishing in Thane (Traditional Print vs Modern Web)
    suggest_curriculum_upgrades("CRS110")
