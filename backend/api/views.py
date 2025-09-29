from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, AccountSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Account
from .filters import AccountFilter
from .favicon_service import FaviconService

class AccountListCreate(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AccountFilter
    search_fields = ['username', 'url', 'notes']
    ordering_fields = ['username', 'url', 'created_at']
    ordering = ['-created_at']  # Default ordering: newest first

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(author=user)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AccountRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(author=user)

    def perform_update(self, serializer):
        """Handle password updates with encryption"""
        if 'password' in serializer.validated_data:
            password = serializer.validated_data.pop('password')
            serializer.save()
            serializer.instance.set_password(password)
            serializer.instance.save()
        else:
            serializer.save()


class AccountDelete(generics.DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Account.objects.filter(author=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Custom login view that accepts username and password"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid username or password.'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetch_favicon(request):
    """Fetch and cache favicon for a given URL"""
    url = request.data.get('url')
    if not url:
        return Response(
            {'error': 'URL is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        favicon_data, content_type = FaviconService.fetch_and_process_favicon(url)
        if favicon_data:
            import base64
            favicon_b64 = base64.b64encode(favicon_data).decode('utf-8')
            favicon_url = f"data:{content_type};base64,{favicon_b64}"
            
            return Response(
                {
                    'success': True,
                    'favicon_url': favicon_url,
                    'content_type': content_type,
                    'size_bytes': len(favicon_data)
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'success': False,
                    'error': 'Could not fetch favicon for the given URL.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': f'Error fetching favicon: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fetch_account_favicon(request, pk):
    """Fetch and cache favicon for a specific account"""
    try:
        account = Account.objects.get(pk=pk, author=request.user)
        
        if account.fetch_favicon():
            favicon_url = account.get_favicon_url()
            return Response(
                {
                    'success': True,
                    'favicon_url': favicon_url,
                    'message': 'Favicon fetched and cached successfully.'
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'success': False,
                    'error': 'Could not fetch favicon for this account.'
                },
                status=status.HTTP_404_NOT_FOUND
            )
    except Account.DoesNotExist:
        return Response(
            {'error': 'Account not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {
                'success': False,
                'error': f'Error fetching favicon: {str(e)}'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )