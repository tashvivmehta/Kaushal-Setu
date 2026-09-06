"""
Maharashtra Skill Intelligence Platform - Starter Demo
Demonstrating:
1. Obsolete ITI trades with placement < 40% across Maharashtra
2. Emerging industrial job roles in Pune & Chhatrapati Sambhajinagar
3. Critical equipment & trainer gaps reported by MIDC employers
"""

import sys
import pandas as pd

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 1. Load datasets
jobs_df = pd.read_csv("data/job_market_demand.csv")
courses_df = pd.read_csv("data/existing_courses.csv")
feedback_df = pd.read_csv("data/employer_feedback.csv")

print("=" * 70)
print("[1] OUTDATED / LOW PLACEMENT ITI TRADES IN MAHARASHTRA (< 40%)")
print("=" * 70)
low_placement = courses_df[courses_df["placement_rate_pct"] < 40]
for _, row in low_placement.iterrows():
    print(f">> Trade: {row['course_name']}")
    print(f"   Institute: {row['institution_name']} | District: {row['district']}")
    print(f"   Placement Rate: {row['placement_rate_pct']}% | Equipment: {row['equipment_status']} | Syllabus Year: {row['curriculum_last_revised_year']}\n")

print("=" * 70)
print("[2] HIGH-DEMAND EMERGING ROLES IN PUNE INDUSTRIAL BELT (Chakan/Bhosari/Hinjewadi)")
print("=" * 70)
pune_jobs = jobs_df[jobs_df["district"] == "Pune"].sort_values(by="open_vacancies", ascending=False)
for _, row in pune_jobs.iterrows():
    print(f">> Role: {row['job_title']} ({row['industrial_cluster']})")
    print(f"   Vacancies: {row['open_vacancies']} | Avg Salary: Rs. {row['avg_monthly_salary_inr']}/month")
    print(f"   Required Skills: {row['required_skills']}\n")

print("=" * 70)
print("[3] WHAT MAHARASHTRA EMPLOYERS REPORT AS CRITICAL MISSING LAB EQUIPMENT")
print("=" * 70)
for _, row in feedback_df.iterrows():
    print(f">> {row['company_name']} ({row['industrial_cluster']}, {row['district']})")
    print(f"   Graduate Readiness Score: {row['candidate_readiness_score']}/5")
    print(f"   Missing Skills: {row['critical_missing_skills']}")
    print(f"   Urgent Lab Upgrade: {row['recommended_new_equipment']}\n")
