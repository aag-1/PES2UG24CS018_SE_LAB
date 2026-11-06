from hypothesis import given, strategies as st
from student_grades import average_marks, parse_srn, short_name

@given(st.text() | st.none())
def test_average_marks_no_crash(s):
    try:
        average_marks(s)
    except Exception as e:
        assert False, f"average_marks crashed with: {e}"

@given(st.text() | st.none())
def test_parse_srn_no_crash(s):
    try:
        parse_srn(s)
    except Exception as e:
        assert False, f"parse_srn crashed with: {e}"

@given(st.text() | st.none())
def test_short_name_no_crash(s):
    try:
        short_name(s)
    except Exception as e:
        assert False, f"short_name crashed with: {e}"

@given(st.lists(st.integers(0, 100), min_size=1))
def test_average_marks_valid(marks):
    csv = ",".join(str(m) for m in marks)
    assert average_marks(csv) == round(sum(marks) / len(marks), 2)
