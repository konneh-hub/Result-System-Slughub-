from rest_framework import routers
from .views import FacultyViewSet, DepartmentViewSet, ProgrammeViewSet, AcademicSessionViewSet, SemesterViewSet

router = routers.DefaultRouter()
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'programmes', ProgrammeViewSet, basename='programme')
router.register(r'sessions', AcademicSessionViewSet, basename='session')
router.register(r'semesters', SemesterViewSet, basename='semester')

urlpatterns = router.urls
