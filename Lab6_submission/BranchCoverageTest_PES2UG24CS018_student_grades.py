import pytest
from student_grades import letter_grade, final_marks, exam_eligibility

# letter_grade
@pytest.mark.parametrize("marks", [-1, 101])
def test_invalid_marks(marks):
    with pytest.raises(ValueError):
        letter_grade(marks)

@pytest.mark.parametrize("marks, grade", [
    (100, "S"), (90, "S"),
    (89, "A"), (80, "A"),
    (79, "B"), (70, "B"),
    (69, "C"), (60, "C"),
    (59, "D"), (50, "D"),
    (49, "E"), (40, "E"),
    (39, "F"), (0, "F"),
])
def test_letter_grade(marks, grade):
    assert letter_grade(marks) == grade


# final_marks
@pytest.mark.parametrize("internal, external", [(41, 0), (0, 61)])
def test_final_marks_out_of_range(internal, external):
    with pytest.raises(ValueError):
        final_marks(internal, external, False)

def test_final_marks_no_project():
    assert final_marks(30, 50, False) == 80

def test_final_marks_project_not_capped():
    assert final_marks(30, 50, True) == 85

def test_final_marks_project_exactly_100():
    assert final_marks(40, 55, True) == 100

def test_final_marks_project_capped():
    assert final_marks(40, 60, True) == 100


# exam_eligibility
def test_blocked():
    assert exam_eligibility(80, False, True) == "blocked"

@pytest.mark.parametrize("attendance", [75, 100])
def test_eligible(attendance):
    assert exam_eligibility(attendance, True, False) == "eligible"

@pytest.mark.parametrize("attendance", [65, 74])
def test_eligible_with_medical(attendance):
    assert exam_eligibility(attendance, True, True) == "eligible"

def test_detained_no_medical():
    assert exam_eligibility(70, True, False) == "detained"

def test_detained_low_attendance_with_medical():
    assert exam_eligibility(64, True, True) == "detained"
