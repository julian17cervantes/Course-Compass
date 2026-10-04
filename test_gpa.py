from gpa import calculate_gpa

def test_single_course():
    assert calculate_gpa([("A", 3)]) == 4.0

def test_weighted_by_weights():
    assert calculate_gpa([("A", 3), ("C", 1)]) == 3.5

def test_ungraded_courses_are_skipped():
    assert calculate_gpa([("A", 3), (None, 4)]) == 4.0

def test_no_courses_returns_zero():
    assert calculate_gpa([]) == 0.0