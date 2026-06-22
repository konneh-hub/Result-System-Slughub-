from apps.grading.models import GradingScheme, GradingRule


def compute_grade_for_score(score):
    try:
        score = float(score)
    except (TypeError, ValueError):
        return None, None

    rule = GradingRule.objects.filter(min_score__lte=score, max_score__gte=score).order_by('-point').first()
    if not rule:
        return None, None
    return rule.grade, rule.point


def compute_result_entry_grade(result):
    if result.ca_score is None or result.exam_score is None:
        return None, None, None

    total = float(result.ca_score) + float(result.exam_score)
    grade, point = compute_grade_for_score(total)
    return total, grade, point


def compute_cgpa(student_profile):
    results = student_profile.results.filter(grade_point__isnull=False)
    if not results.exists():
        return None

    total_points = 0
    total_credits = 0
    for result in results:
        try:
            credit_units = float(result.offering.course.credit_units)
            grade_point = float(result.grade_point)
        except (TypeError, ValueError):
            continue
        total_points += credit_units * grade_point
        total_credits += credit_units

    if total_credits == 0:
        return None
    return round(total_points / total_credits, 2)
