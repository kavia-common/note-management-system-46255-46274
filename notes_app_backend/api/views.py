from django.contrib.auth import authenticate
from django.db import models
from rest_framework import permissions, status, viewsets, mixins, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Note
from .serializers import NoteSerializer, RegisterSerializer, UserSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health(request):
    """
    Health check endpoint for readiness/liveness probes.
    Returns 200 with a simple payload.
    """
    return Response({"message": "Server is up!"}, status=status.HTTP_200_OK)


class IsOwner(permissions.BasePermission):
    """Permission that allows access only to the owner of the note."""

    def has_object_permission(self, request, view, obj):
        return getattr(obj, "owner_id", None) == getattr(request.user, "id", None)


class StandardResultsSetPagination(pagination.PageNumberPagination):
    """Default pagination: supports page and page_size query params."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


# PUBLIC_INTERFACE
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Register a new user.

    Request body:
    - username: string
    - password: string

    Returns:
    - 201 with {"user": {...}, "token": "<token>"} on success.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {"user": UserSerializer(user).data, "token": token.key},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUBLIC_INTERFACE
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Login a user using username and password.

    Request body:
    - username: string
    - password: string

    Returns:
    - 200 with {"user": {...}, "token": "<token>"} if valid.
    - 400 if invalid credentials.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"detail": "username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({"user": UserSerializer(user).data, "token": token.key}, status=status.HTTP_200_OK)


class NoteViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet for CRUD operations on notes.

    Authentication: Token
    Permissions: Authenticated users; object-level access for owners only.

    Query params for list:
    - q: search string on title/content
    - page, page_size: pagination controls
    """
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        qs = Note.objects.filter(owner=self.request.user)
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(models.Q(title__icontains=q) | models.Q(content__icontains=q))
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
