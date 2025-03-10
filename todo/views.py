from .models import Todo
from datetime import datetime
from rest_framework import status
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def todo_list(request):
    date = request.query_params.get('date')
    is_completed = request.query_params.get('is_completed') 
    
    if not date:
        return Response({"error": "날짜가 필요합니다. YYYY-MM-DD 형식으로 전달해주세요."}, status=status.HTTP_400_BAD_REQUEST)     
    try:
        select_date = datetime.strptime(date, "%Y-%m-%d").date() 

    except ValueError:
        return Response({"error": "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 전달해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    todo = Todo.objects.filter(select_date=select_date, user=request.user).order_by("created_at") 

    if is_completed is not None: 
        todo = todo.filter(is_completed=(is_completed.lower() == 'true')) 
    
    serializer = TodoSerializer(todo, many=True) 
    return Response(serializer.data, status=status.HTTP_200_OK)