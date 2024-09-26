import pytest
from src.icd_code_determiner import determine_icd_code, get_full_row_by_code

@pytest.mark.parametrize("input_text, expected_code", [
    # Existing tests
    ("Chronic pulmonary histoplasmosis capsulati", "B391"),
    ("Pulmonary histoplasmosis capsulati, unspecified", "B392"),
    ("Disseminated histoplasmosis capsulati", "B393"),
    ("Histoplasmosis capsulati, unspecified", "B394"),
    ("Histoplasmosis duboisii", "B395"),
    ("Histoplasmosis, unspecified", "B399"),
    ("Acute pulmonary blastomycosis", "B400"),
    ("Chronic pulmonary blastomycosis", "B401"),
    ("Pulmonary blastomycosis, unspecified", "B402"),
    ("Cutaneous blastomycosis", "B403"),
    ("Disseminated blastomycosis", "B407"),
    ("Blastomycotic meningoencephalitis", "B4081"),
    ("Other forms of blastomycosis", "B4089"),
    ("Blastomycosis, unspecified", "B409"),
    ("Pulmonary paracoccidioidomycosis", "B410"),
    ("Disseminated paracoccidioidomycosis", "B417"),
    ("Other forms of paracoccidioidomycosis", "B418"),
    ("Paracoccidioidomycosis, unspecified", "B419"),
    ("Pulmonary sporotrichosis", "B420"),
    ("Lymphocutaneous sporotrichosis", "B421"),
    ("Disseminated sporotrichosis", "B427"),
    ("Cerebral sporotrichosis", "B4281"),
    
    # New tests from additional groups
    ("Adenovirus as the cause of diseases classified elsewhere", "B970"),
    ("Coxsackievirus as the cause of diseases classified elsewhere", "B9711"),
    ("Echovirus as the cause of diseases classified elsewhere", "B9712"),
    ("SARS-associated coronavirus as the cause of diseases classified elsewhere", "B9721"),
    ("Lentivirus as the cause of diseases classified elsewhere", "B9731"),
    ("HTLV-I as the cause of diseases classified elsewhere", "B9733"),
    ("HIV 2 as the cause of diseases classified elsewhere", "B9735"),
    ("Respiratory syncytial virus as the cause of diseases classified elsewhere", "B974"),
    ("Reovirus as the cause of diseases classified elsewhere", "B975"),
    ("Human metapneumovirus as the cause of diseases classified elsewhere", "B9781"),
    ("Other infectious disease", "B998"),
    
    ("Malignant neoplasm of bones of skull and face", "C410"),
    ("Malignant neoplasm of vertebral column", "C412"),
    ("Malignant neoplasm of pelvic bones, sacrum and coccyx", "C414"),
    ("Malignant melanoma of lip", "C430"),
    ("Malignant melanoma of right upper eyelid, including canthus", "C43111"),
    ("Malignant melanoma of left lower eyelid, including canthus", "C43122"),
    ("Malignant melanoma of scalp and neck", "C434"),
    ("Malignant melanoma of anal skin", "C4351"),
    ("Malignant melanoma of other part of trunk", "C4359"),
    ("Malignant melanoma of right lower limb, including hip", "C4371"),
    ("Malignant melanoma of overlapping sites of skin", "C438"),
    
    ("Malignant neoplasm of axillary tail of right female breast", "C50611"),
    ("Malignant neoplasm of axillary tail of left male breast", "C50622"),
    ("Malignant neoplasm of overlapping sites of right female breast", "C50811"),
    ("Malignant neoplasm of unspecified site of left female breast", "C50912"),
    ("Malignant neoplasm of labium majus", "C510"),
    ("Malignant neoplasm of clitoris", "C512"),
    ("Malignant neoplasm of vagina", "C52"),
    ("Malignant neoplasm of endocervix", "C530"),
    ("Malignant neoplasm of fundus uteri", "C543"),
    ("Malignant neoplasm of bilateral ovaries", "C563"),
    ("Malignant neoplasm of right fallopian tube", "C5701"),
    ("Malignant neoplasm of left round ligament", "C5722"),
    ("Malignant neoplasm of placenta", "C58"),
])
def test_icd_codes_extended(input_text, expected_code, capsys):
    code = determine_icd_code(input_text)
    full_row = get_full_row_by_code(code)
    print(f"Input: {input_text}")
    print(f"Expected Code: {expected_code}")
    print(f"Actual Code: {code}")
    print(f"Full row: {full_row}")
    captured = capsys.readouterr()
    print(captured.out)
    assert code == expected_code, f"Mismatch for input '{input_text}'"
    assert len(full_row) > 0, f"No full row found for code {code}"

def test_partial_matches():
    assert determine_icd_code("chronic histoplasmosis") == "B391"
    assert determine_icd_code("unspecified blastomycosis") == "B409"
    assert determine_icd_code("coronavirus as the cause of diseases") == "B9729"
    assert determine_icd_code("malignant melanoma of eyelid") in ["C43111", "C43112", "C43121", "C43122"]
    assert determine_icd_code("malignant neoplasm of breast") in ["C50811", "C50812", "C50911", "C50912"]

def test_case_insensitivity():
    assert determine_icd_code("ACUTE PULMONARY BLASTOMYCOSIS") == "B400"
    assert determine_icd_code("htlv-i as the cause of diseases") == "B9733"
    assert determine_icd_code("MALIGNANT MELANOMA OF LIP") == "C430"

def test_multiple_possible_matches():
    assert determine_icd_code("pulmonary histoplasmosis") in ["B391", "B392"]
    assert determine_icd_code("malignant neoplasm of female breast") in ["C50611", "C50612", "C50811", "C50812", "C50911", "C50912"]
    assert determine_icd_code("malignant melanoma of eyelid") in ["C43111", "C43112", "C43121", "C43122"]

def test_no_match():
    assert determine_icd_code("common cold") == "R69"
    assert determine_icd_code("unspecified viral infection") == "R69"
    assert determine_icd_code("benign tumor") == "R69"

def test_similar_terms():
    assert determine_icd_code("lung histoplasmosis") in ["B391", "B392"]
    assert determine_icd_code("skin blastomycosis") == "B403"
    assert determine_icd_code("breast cancer") in ["C50611", "C50612", "C50811", "C50812", "C50911", "C50912"]
    assert determine_icd_code("cervical cancer") in ["C530", "C531", "C538", "C539"]

def test_full_row_retrieval():
    code = "B391"
    full_row = get_full_row_by_code(code)
    assert len(full_row) > 0
    assert "Chronic pulmonary histoplasmosis capsulati" in full_row[1]

    code = "C430"
    full_row = get_full_row_by_code(code)
    assert len(full_row) > 0
    assert "Malignant melanoma of lip" in full_row[1]

def test_performance():
    import time
    start_time = time.time()
    for _ in range(1000):
        determine_icd_code("Chronic pulmonary histoplasmosis capsulati")
        determine_icd_code("Malignant melanoma of lip")
        determine_icd_code("HIV 2 as the cause of diseases classified elsewhere")
    end_time = time.time()
    assert end_time - start_time < 1, "Performance test failed: took more than 1 second for 3000 determinations"