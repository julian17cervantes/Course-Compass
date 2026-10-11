import pytest

from gpa import calculate_gpa, final_score_needed, required_gpa

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

def test_final_score_achievable():
    # (85 - 90 * 0.8) / 0.2 = 65
    result = final_score_needed(90, 20, 85)
    assert result["status"] == "achievable"
    assert result["needed_on_final"] == 65.0


def test_final_score_impossible():
    # (90 - 70 * 0.7) / 0.3 = 136.67, more than 100%
    result = final_score_needed(70, 30, 90)
    assert result["status"] == "impossible"


def test_final_score_already_met():
    result = final_score_needed(100, 20, 70)
    assert result["status"] == "already_met"
    assert result["needed_on_final"] == 0.0


def test_final_score_rejects_bad_weight():
    with pytest.raises(ValueError):
        final_score_needed(90, 0, 85)