# SIH Skill Intelligence Platform - Starter Datasets

These datasets are crafted for your Smart India Hackathon problem statement. They represent realistic data from Indian vocational training institutes (ITIs), job market demand across key districts, and employer surveys.

## 📁 Files Overview

### 1. `data/job_market_demand.csv` (What Industry Needs)
Contains real-world job roles and the actual skills companies are currently hiring for.
* **Key Columns:**
  * `job_title`: Name of the job (e.g., Solar Installation Technician, EV Battery Technician, Data Analyst).
  * `sector`: Industry sector (Renewable Energy, Automotive, IT, Healthcare, etc.).
  * `district` & `state`: Geographic location (Jaipur, Pune, Lucknow, Coimbatore, Indore).
  * `required_skills`: Skills listed in job postings.
  * `proficiency_level`: Beginner, Intermediate, Advanced.
  * `avg_monthly_salary_inr`: Expected monthly salary in ₹.
  * `open_vacancies`: Number of openings.
  * `emerging_trend_score`: Score from 1 to 10 on how fast this demand is rising.

### 2. `data/existing_courses.csv` (What Institutes Currently Teach)
Contains real-world vocational training courses from ITIs and training centers.
* **Key Columns:**
  * `course_name`: Name of the course (e.g., COPA, Electrician, DTP Operator).
  * `institution_name`: College or training center.
  * `district`: Where the institute is located.
  * `skills_taught`: Syllabus items currently taught.
  * `duration_months`: Course length.
  * `placement_rate_pct`: % of students who got jobs (low % = red flag / obsolete course).
  * `trainer_capacity_score`: Rating (1-5) on how prepared the trainers are.
  * `equipment_status`: Outdated, Moderate, or Modern.
  * `curriculum_last_revised_year`: When syllabus was last updated.

### 3. `data/employer_feedback.csv` (Industry Validation & Surveys)
Direct feedback from employers regarding graduate readiness and missing skills.
* **Key Columns:**
  * `company_name`: Local employer name.
  * `candidate_readiness_score`: Rating (1-5) of recent graduates.
  * `critical_missing_skills`: What skills graduates lack when interviewed.
  * `urgent_trainer_training_needed`: Whether college teachers need retraining (Yes/No).
  * `recommended_new_equipment`: What modern machines/labs colleges need to buy.
  * `willing_to_offer_apprenticeship`: Industry willingness to partner (Yes/No).
