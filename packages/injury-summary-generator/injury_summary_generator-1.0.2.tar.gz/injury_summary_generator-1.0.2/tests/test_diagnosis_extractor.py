from src.diagnosis_extractor import extract_diagnosis

def test_extract_diagnosis_with_primary_diagnosis():
    text = """
    Assessment:
    Primary Diagnosis: Fracture of the lower leg.
    """
    assert extract_diagnosis(text) == 'Fracture of the lower leg.'

def test_extract_diagnosis_with_prognosis():
    text = """
    Assessment:
    Prognosis: Right ankle sprain with possible involvement of the joint of the right foot.
    """
    assert extract_diagnosis(text) == 'Right ankle sprain with possible involvement of the joint of the right foot.'

def test_extract_diagnosis_with_diagnosis():
    text = """
    Assessment:
    Diagnosis: Severe sprain of the wrist.
    """
    assert extract_diagnosis(text) == 'Severe sprain of the wrist.'

def test_extract_diagnosis_from_chief_complaint():
    text = """
    Chief Complaint: Persistent cough and fever.
    
    Assessment:
    No clear diagnosis at this time.
    """
    assert extract_diagnosis(text) == 'Persistent cough and fever.'

def test_extract_diagnosis_no_diagnosis():
    text = """
    No relevant medical information provided.
    """
    assert extract_diagnosis(text) == "Illness unspecified"

def test_extract_diagnosis_empty_text():
    text = ""
    assert extract_diagnosis(text) == "Illness unspecified"

def test_extract_diagnosis_with_colon_in_diagnosis():
    text = """
    Assessment:
    Primary Diagnosis: Complex regional pain syndrome: upper limb.
    """
    assert extract_diagnosis(text) == 'Complex regional pain syndrome: upper limb.'

def test_extract_diagnosis_with_multiline_assessment():
    text = """
    Assessment:
    Primary Diagnosis: Chronic obstructive pulmonary disease (COPD)
    with acute exacerbation.
    Secondary: Hypertension
    """
    assert extract_diagnosis(text) == 'Chronic obstructive pulmonary disease (COPD) with acute exacerbation.'