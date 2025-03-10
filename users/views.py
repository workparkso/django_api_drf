from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from .serializers import UserCreateSerializer

User = get_user_model() # 이거 사용하는 이유:


# create : 사용자를 생성
@api_view(['POST']) 
@authentication_classes([])  
@permission_classes([AllowAny])
def user_create(request):
    serializer = UserCreateSerializer(data=request.data) # UserCreateSerializer으로 유효성을 검사
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": f"{serializer.data['username']}님 회원가입이 정상적으로 완료되었습니다.",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  
  
  
  