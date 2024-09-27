import pytest
from src.icd_code_determiner import determine_icd_code, get_full_row_by_code

def test_exact_match(capsys):
    diagnosis = "Cholera due to Vibrio cholerae 01, biovar cholerae"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A000"
    assert len(full_row) > 0

    diagnosis = "Malignant carcinoid tumor of the midgut, unspecified"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "C7A095"
    assert len(full_row) > 0

    diagnosis = "Leukemia, unspecified, in remission"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "C9591"
    assert len(full_row) > 0

def test_partial_match(capsys):
    diagnosis = "Leukemia unspecified in remission"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "C9591"  # Whithot comas
    assert len(full_row) > 0

    diagnosis = "Diagnosed with typhoid"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A0100"  # Unspecified typhoid fever
    assert len(full_row) > 0

    diagnosis = "Salmonella infection detected"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A029"  # Unspecified salmonella infection
    assert len(full_row) > 0

def test_case_insensitivity(capsys):
    diagnosis = "CHOLERA DUE TO VIBRIO CHOLERAE 01, BIOVAR CHOLERAE"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A000"
    assert len(full_row) > 0

    diagnosis = "typhoid fever, unspecified"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A0100"
    assert len(full_row) > 0

def test_multiple_possible_matches(capsys):
    diagnosis = "Typhoid fever with pneumonia"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A0103"  # Should prefer more specific code
    assert len(full_row) > 0

    diagnosis = "Salmonella infection in the lungs"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A0222"  # Salmonella pneumonia
    assert len(full_row) > 0

def test_no_match(capsys):
    diagnosis = "Common cold"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "R69"  # Should return unspecified illness code
    assert len(full_row) > 0

    diagnosis = "Patient feeling tired"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "R69"
    assert len(full_row) > 0

def test_similar_terms(capsys):
    diagnosis = "Intestinal infection caused by E. coli"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A049"  # Unspecified bacterial intestinal infection
    assert len(full_row) > 0

    diagnosis = "Food poisoning"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A059"  # Unspecified bacterial foodborne intoxication
    assert len(full_row) > 0

def test_complex_cases(capsys):
    diagnosis = "Patient presents with fever, abdominal pain, and diarrhea. Suspect typhoid."
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A0100"
    assert len(full_row) > 0

    diagnosis = "Chronic cough and weight loss, possible tuberculosis"
    code = determine_icd_code(diagnosis)
    full_row = get_full_row_by_code(code)
    print(f"Diagnosis: {diagnosis}")
    print(f"Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == "A159"  # Unspecified respiratory tuberculosis
    assert len(full_row) > 0

@pytest.mark.parametrize("input_text, expected_code", [
    ("Cholera due to Vibrio cholerae 01, biovar cholerae", "A000"),
    ("Typhoid fever, unspecified", "A0100"),
    ("Salmonella enteritis", "A020"),
    ("Patient has cholera", "A009"),
    ("CHOLERA DUE TO VIBRIO CHOLERAE 01, BIOVAR CHOLERAE", "A000"),
    ("Typhoid fever with pneumonia", "A0103"),
    ("Common cold", "R69"),
    ("Intestinal infection caused by E. coli", "A049"),
    ("Chronic cough and weight loss, possible tuberculosis", "A159"),
])
def test_icd_codes_parametrized(input_text, expected_code, capsys):
    code = determine_icd_code(input_text)
    full_row = get_full_row_by_code(code)
    print(f"Input: {input_text}")
    print(f"Expected Code: {expected_code}")
    print(f"Actual Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)  # This will be visible even with output capture
    assert code == expected_code, f"Mismatch for input '{input_text}'"

def test_performance():
    import time
    start_time = time.time()
    for _ in range(1000):
        determine_icd_code("Cholera due to Vibrio cholerae 01, biovar cholerae")
    end_time = time.time()
    assert end_time - start_time < 1  # Тест должен выполниться менее чем за 1 секунду