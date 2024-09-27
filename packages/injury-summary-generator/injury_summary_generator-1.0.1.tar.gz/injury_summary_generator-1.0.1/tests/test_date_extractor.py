from src.date_extractor import extract_date

def test_extract_date_valid_iso():
    text = """
    Patient was seen on 20 23-01-01. 
    """
    assert extract_date(text) == '2023-01-01'

def test_extract_date_valid_long_format():
    text = """
    The appointment was on January 15, 2021.
    """
    assert extract_date(text) == '2021-01-15'

def test_extract_date_valid_different_format():
    text = """
    Visit Date: 15 Jan 2021
    """
    assert extract_date(text) == '2021-01-15'

def test_extract_date_no_date():
    text = """
    No date information here.
    """
    assert extract_date(text) == "Date not found"

def test_extract_date_excluded_dob():
    text = """
    Date of Birth: 15 Jan 1 980
    Visit Date: 23 Apr 2023
    """
    assert extract_date(text) == '2023-04-23'

def test_extract_date_invalid_date():
    text = """
    The date mentioned is 32/13/2020, which is invalid.
    """
    assert extract_date(text) == "Date not found"

def test_extract_date_multiple_dates():
    text = """
    Patient was born on 198 0-05-20 and was seen on 2023-07-15.
    """
    assert extract_date(text) == '2023-07-15'

def test_extract_date_with_context():
    text = """
    This is a test PDF document. 
If you can read this, you have Adobe Acrobat Reader installed on your computer. 
    """
    assert extract_date(text) == 'Date not found'

def test_extract_date_with_extra_text():
    text = """
    Date of Birth: January 15, 198 5
Gender: Male
Patient ID: 123456
Date of Visit: Dec 5, 2L19
Chief Complaint:
Pain in the neck with radiating pain to the arm
    """
    assert extract_date(text) == '2019-12-05'
    
def test_extract_date_with_time():
    text = """
    Name: John Doe
Date of Birth: Ja nuary 15, 1985
Gender: Male
Patient ID: 123456
Date of Visit: March 8, 20O0
Chief Complaint:
Pain in the neck and upper back
History of Present Illness (HPI):
Onset: The pain started approximately 1 month ago.
Location: Cervical region (neck and upper back).
Duration: Persistent, worsening over time.
Characteristics: Dull, aching pain with occasional sharp, shooting pains down the arms.  
Aggravating Factors: Prolonged sitting, certain neck movements.
Relieving Factors: Rest, over-the-counter pain medications, gentle neck exercises.  
Associated Symptoms: Numbness and tingling in the arms, occasional headaches.  
    """
    assert extract_date(text) == '2000-03-08'
    
def test_extract_date_with_relative_date():
    text = """
    Name: John Doe
Date of Birth: January 15, 1985
Gender: Male
Patient ID: 123456
Visited: 20/08/2020
Chief Complaint:
Pain in the right ankle and joint of the right foot
History of Present Illness (HPI):
Onset: The pain started approximately 3 weeks ago after a minor sprain.
Location: Right ankle and joint of the right foot.
Duration: Persistent, worsening with activity.
Characteristics: Sharp, throbbing pain with swelling and tenderness.
Aggravating Factors: Walking, standing for long periods, and physical activity.
Relieving Factors: Rest, ice application, elevation, and over-the-counter pain medications (ibuprofen).  
Associated Symptoms: Swelling, stiffness, and occasional bruising.
Past Medical History:
Chronic Conditions: Hypertension, Type 2 Diabetes.
Previous Surgeries: Appendectomy (2010).
    """
    assert extract_date(text) == '2020-08-20'

def test_extract_date_corrupted_data():
    text = """
   Visit 1  
P
a�ent Informa�on:  
•Name: John Doe
•Date of Birth: December 15,  1972
•Gender: Male
•Pa�ent ID: 123456
•Visit date: 07/26/2 021
Ch
ief Complaint:  
•Pain in the right shoulder
History of Present Illness (HPI):  
•Onset: The pain started approximately 2 weeks ago.
•Loca�on: Right shoulder
•Dura�on: The pain is persistent, varying in intensity.
•Characteris�cs: Sharp, aching pain; some�mes radiates down the arm.
•Aggrava�ng Factors: Li�ing, overhead ac�vi�es, and certain movements.
•Relieving Factors:  Rest, ice applica�on, over -the-counter pain medica�on (ibuprofen).
•Associated Symptoms:  Occasional numbness and �ngling in the right arm.
Past Medical History:  
•Chronic Condi�ons: Hypertension, Type 2 Diabetes
•Previous Surgeries:  Appendectomy (2010)
•Medica�ons: Me�ormin, Lisinopril, Ibuprofen (as needed for pain)
•Allergies:  No known drug allergies
Social History:  
•Occupa�on: Oﬃce worker
•Smoking: Non -smoker
•Alcohol Use: Occasionally
•Exercise:  Infrequent
Family History:  
• Father: Hypertension, Heart disease  
• Mother: Type 2 Diabetes  
• Siblings:  Healthy  
Review of Systems:  
• General: No fever, no weight loss  
• Musculoskeletal: Pain in the right shoulder, no other joint pain or swelling  
• Neurological:  Occasional numbness and �ngling in the right arm, no other neurological deﬁcits  
• Cardiovascular: No chest pain, no palpita�ons  
• Respiratory: No shortness of breath, no cough  
Physical Examina�on:  
• General: Alert, well- nourished, in no acute distress  
• Vital Signs:  
o Blood Pressure: 130/85 mmHg  
o Heart Rate: 78 bpm  
o Respiratory Rate: 16 breaths/min  
o Temperature: 98.6°F (37°C)  
• Inspec�on: No obvious deformi�es, swelling, or redness in the right shoulder  
• Palpa�on: Tenderness over the right shoulder, par�cularly at the anterior aspect  
• Range of Mo�on: Limited due to pain, especially in abduc�on and external rota�on  
• Strength: 4/5 in the right shoulder, normal strength in the le� shoulder  
• Special Tests:  Posi�ve Neer’s and Hawkins -Kennedy tests indica�ng possible impingement 
syndrome  
Assessment:  
• Primary Diagnosis: Right shoulder impingement syndrome  
• Diﬀeren�al Diagnoses:  Rotator cuﬀ tear, bursi�s, tendini�s, cervical radiculopathy  
Plan: 
1. Imaging: Order X -ray and MRI of the right shoulder to evaluate the extent of the injury.  
2. Medica�ons: Con�nue ibuprofen for pain management; consider prescribing physical therapy.  
3. Referral:  Refer to orthopedic specialist for further evalua�on.  
4. Ac�vity:  Advise pa�ent to avoid ac�vi�es that exacerbate pain; recommend gentle stretching 
exercises.  
5. Follow -Up: Schedule follow -up appointment in 2 weeks to review imaging results and assess 
response to treatment.  
Pa�ent Educa�on: 
• Discussed the nature of the condi�on, poten�al causes, and treatment op�ons.  
• Instructed on proper use of medica�on and importance of adhering to prescribed therapy.  
• Encouraged pa�ent to report any worsening symptoms or new concerns.  
    """
    assert extract_date(text) == '2021-07-26'