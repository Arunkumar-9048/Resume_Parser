from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Resume, Candidate
from .serializer import CandidateSerializer, EmployeeSerializer
from .utils import extract_text, parse_resume

# Create your views here.

class ParseResumeAPIView(APIView):
    
    def post(self, request):

        file= request.FILES.get('resume')
        if not file:
            return Response({"error": "NO file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
    
        resume_obj = Resume.objects.create(file=file)
        
        text = extract_text(file)
        
        parsed_data = parse_resume(text)
        
        Candidate_obj = Candidate.objects.create(
            resume= resume_obj,
            full_name= parsed_data.get("full_name", ""),
            email=parsed_data.get("email", ""),
            phone=parsed_data.get("phone", ""),
            location=parsed_data.get("location", ""),
            experience=parsed_data.get("experience", ""),
            linkedin=parsed_data.get("linkedin", "")
        )
        
        serializer = CandidateSerializer(Candidate_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class EmployeeCreateAPIView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Employee created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
