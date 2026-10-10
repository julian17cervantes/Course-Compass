from gpa import calculate_gpa, required_gpa

def test_single_course():
    assert calculate_gpa([("A", 3)]) == 4.0

def test_weighted_by_weights():
    assert calculate_gpa([("A", 3), ("C", 1)]) == 3.5

def test_ungraded_courses_are_skipped():
    assert calculate_gpa([("A", 3), (None, 4)]) == 4.0

def test_no_courses_returns_zero():
    assert calculate_gpa([]) == 0.0

def test_required_gpa_achievable():
    result = required_gpa(3.5, [("A", 3), (None, 3)])
    assert result["status"] == "achievable"
    assert result["required_average"] == 3.0
    assert result["minimum_letter"] == "B"


def test_required_gpa_impossible():
    result = required_gpa(4.0, [("C", 3), (None, 3)])
    assert result["status"] == "impossible"


def test_required_gpa_already_met():
    result = required_gpa(2.0, [("A", 30), (None, 3)])
    assert result["status"] == "already_met"


def test_required_gpa_no_upcoming_courses():
    result = required_gpa(3.5, [("B", 3)])
    assert result["status"] == "no_upcoming_courses"