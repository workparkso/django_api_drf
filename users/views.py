from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny # 권한
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserCreateSerializer


User = get_user_model() # 이거 사용하는 이유:


# create : 사용자를 생성하는 API
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
  
  
# 로그인
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"error": "이메일과 비밀번호를 모두 입력해주세요."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(request, email=email, password=password)

    if user is not None: 
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": f"{user.username}님, 반갑습니다!",
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "이메일 또는 비밀번호가 올바르지 않습니다."}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

  
  
  
# 로그아웃
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def logout(request):
    try:
        refresh_token = request.data['refresh']

        if not refresh_token:
            return Response({"error": "Refresh token가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "로그아웃 성공"}, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"error": "로그아웃 실패", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
      
      
#계정탈퇴
@api_view(['DELETE'])
def delete_account(request):
    user = request.user
    if not user:
        return Response({"error": "회원 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    password = request.data.get('password')
    if not password:
        return Response({"error": "비밀번호를 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(password):
        return Response({"error": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        RefreshToken.for_user(user).blacklist()
        user.delete()
        return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": f"회원 탈퇴 중 오류가 발생했습니다: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  