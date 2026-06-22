from django.utils import timezone

from apps.reports.models import ReportRequest
from apps.students.models import StudentProfile
from apps.results.models import ResultEntry
from apps.academics.models import Programme


def build_student_performance_report(request_obj: ReportRequest):
    params = request_obj.parameters or {}
    programme_id = params.get('programme_id')
    semester_id = params.get('semester_id')

    students = StudentProfile.objects.all()
    if programme_id:
        students = students.filter(programme_id=programme_id)

    results = ResultEntry.objects.filter(is_published=True)
    if semester_id:
        results = results.filter(offering__semester_id=semester_id)

    summary = []
    for student in students:
        student_results = results.filter(student=student)
        average_grade = None
        total = student_results.count()
        if total:
            total_points = sum((float(r.grade_point or 0) * float(r.offering.course.credit_units or 0)) for r in student_results)
            total_credits = sum(float(r.offering.course.credit_units or 0) for r in student_results)
            average_grade = round(total_points / total_credits, 2) if total_credits else None
        summary.append({
            'student': str(student),
            'programme': student.programme.name if student.programme else None,
            'completed_results': total,
            'average_point': average_grade,
        })

    request_obj.payload = {'summary': summary}
    request_obj.status = 'completed'
    request_obj.completed_at = request_obj.completed_at or timezone.now()
    request_obj.save(update_fields=['payload', 'status', 'completed_at'])
    return request_obj.payload
