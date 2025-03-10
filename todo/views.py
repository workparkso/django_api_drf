from .models import Todo
from datetime import datetime
from rest_framework import status
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# 할 일 리스트
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
  
  
# 체크 박스(한일 안한일 구분하기 위한 체크박스스)
@api_view(['PATCH'])
def todo_checkbox(request):
    date = request.query_params.get('date') 
    todo_id = request.query_params.get('todo_id') 

    if not date or not todo_id:
        return Response({"error": "날짜와 할 일 ID가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        select_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "날짜 형식이 올바르지 않습니다. YYYY-MM-DD 형식으로 전달해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    try: 
        todo = Todo.objects.get(pk=todo_id, select_date=select_date, user=request.user) # Todo 모델에서 todo_id, select_date, 그리고 현재 로그인된 사용자의 정보에 해당하는 할 일을 찾기
    except Todo.DoesNotExist:
        return Response({"error": "해당 조건에 맞는 todo를 찾을 수 없습니다. "}, status=status.HTTP_404_NOT_FOUND)
    
    todo.is_completed = not todo.is_completed   # 할 일의 완료 여부를 반전 a = not a 로 해서 결국에는 not a 인 것과 같은 원리
    todo.save()  # todo 객체를 데이터베이스에 저장

    serializer = TodoSerializer(todo)  # Todo 객체를 직렬화하여 JSON 형식으로 변환
    return Response(serializer.data, status=status.HTTP_200_OK)


# 할일 생성
@api_view(['POST'])
def todo_create(request):
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user) 
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 할일 삭제
@api_view(['DELETE'])
def todo_delete(request, todo_id):
    try:
        todo = Todo.objects.get(pk=todo_id, user=request.user) 
    except Todo.DoesNotExist:
        return Response({"error": "Todo를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    todo.delete()
    return Response({"message": "Todo 리스트를 성공적으로 삭제했습니다."})
  
  
  