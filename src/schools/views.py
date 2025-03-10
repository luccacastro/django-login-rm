from rest_framework.views import APIView
from rest_framework.response import Response
from schools.models import School
from accounts.models import CustomUser

class SchoolListAPIView(APIView):
    def get(self, request):
        schools = School.objects.all().values('id', 'name')
        return Response(schools)
