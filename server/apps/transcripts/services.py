from django.utils import timezone

from apps.transcripts.models import TranscriptRequest
from apps.results.models import ResultEntry


def build_transcript_payload(request_obj: TranscriptRequest):
    student = request_obj.student
    results = ResultEntry.objects.filter(student=student, is_published=True).select_related('offering__course', 'offering__semester', 'offering__programme')
    transcript_results = []
    for r in results:
        transcript_results.append({
            'course': r.offering.course.title,
            'course_code': r.offering.course.code,
            'programme': r.offering.programme.name if r.offering.programme else None,
            'semester': r.offering.semester.name if r.offering.semester else None,
            'year': r.offering.year,
            'grade': r.grade,
            'grade_point': float(r.grade_point or 0),
            'credit_units': float(r.offering.course.credit_units or 0),
            'total_score': float(r.total_score or 0),
        })

    payload = {
        'student': str(student),
        'matric_no': student.matric_no,
        'programme': student.programme.name if student.programme else None,
        'results': transcript_results,
    }
    request_obj.payload = payload
    request_obj.status = 'completed'
    request_obj.generated_at = request_obj.generated_at or timezone.now()
    request_obj.save(update_fields=['payload', 'status', 'generated_at'])
    return payload
