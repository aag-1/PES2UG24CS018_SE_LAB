import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

# letter_grade
def test_invalid_marks():
    with pytest.raises(ValueError):
        letter_grade(-1)

def test_s_grade():
    assert letter_grade(95) == "S"

def test_a_grade():
    assert letter_grade(85) == "A"

def test_b_grade():
    assert letter_grade(75) == "B"

def test_c_grade():
    assert letter_grade(65) == "C"

def test_d_grade():
    assert letter_grade(55) == "D"

def test_e_grade():
    assert letter_grade(45) == "E"

def test_f_grade():
    assert letter_grade(30) == "F"


# final_marks
def test_final_marks_out_of_range():
    with pytest.raises(ValueError):
        final_marks(41, 0, False)

def test_final_marks_project_capped():
    assert final_marks(40, 60, True) == 100


# exam_eligibility
def test_blocked():
    assert exam_eligibility(80, False, False) == "blocked"

def test_eligible():
    assert exam_eligibility(80, True, False) == "eligible"

def test_eligible_with_medical():
    assert exam_eligibility(70, True, True) == "eligible"

def test_detained():
    assert exam_eligibility(70, True, False) == "detained"
