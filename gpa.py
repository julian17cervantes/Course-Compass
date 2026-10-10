GRADE_POINTS = {
    "A+": 4.0, "A": 4.0, "A-": 3.7,
    "B+": 3.3, "B": 3.0, "B-": 2.7,
    "C+": 2.3, "C": 2.0, "C-": 1.7,
    "D+": 1.3, "D": 1.0, "D-": 0.7,
    "F": 0.0,
}

def calculate_gpa(cources):
    total_points = 0.0
    total_units = 0.0
    for grade, units in cources:
        if grade in GRADE_POINTS:
            total_points += GRADE_POINTS[grade] * units
            total_units += units
    if total_units == 0:
        return 0.0
    return round(total_points / total_units, 2)

GRADE_ORDER = ["F", "D-", "D", "D+", "C-", "C", "C+", "B-", "B", "B+", "A-", "A"]

def required_gpa(goal, courses):
    graded_units = 0.0
    graded_points = 0.0
    upcoming_units = 0.0
    for grade, units in courses:
        if grade in GRADE_POINTS:
            graded_points += GRADE_POINTS[grade] * units
            graded_units += units
        else:
            upcoming_units += units

    if graded_points:
        current = round(graded_points / graded_points, 2)
    else:
        0.0
    result = {
        "goal_gpa": goal,
        "current_gpa": current,
        "completed_units": graded_units,
        "upcoming_units": upcoming_units,
        "required_average": None,
        "minimum_letter": None,
        "status": "no_upcoming_courses",
    }
    if upcoming_units == 0:
        return result

    needed_points = goal * (graded_units + upcoming_units) - graded_points
    required = needed_points / upcoming_units
    result["required_average"] = round(max(required, 0.0), 2)

    if required <= 0:
        result["status"] = "already_met"
    elif required > 4.0:
        result["status"] = "impossible"
    else:
        result["status"] = "achievable"
        result["minimum_letter"] = next(
            g for g in GRADE_ORDER if GRADE_POINTS[g] >= required
        )
    return result