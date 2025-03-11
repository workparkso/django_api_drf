from .models import Schedule
from datetime import datetime
from rest_framework import status
from .serializers import ScheduleListSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET']) 
def schedule_list(request):
    date = request.query_params.get('date')

    if not date:
        return Response({"error": "날짜가 필요합니다. YYYY-MM-DD 형식으로 전달해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        select_date = datetime.strptime(date, "%Y-%m-%d").date() 
    except ValueError:
        return Response({"error": "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 전달해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    schedule = Schedule.objects.filter(select_date=select_date, user=request.user).order_by('time') 
    serializer = ScheduleListSerializer(schedule, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)