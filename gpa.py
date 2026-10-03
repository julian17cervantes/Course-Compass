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