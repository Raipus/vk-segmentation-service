from django.shortcuts import render
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from segments.models import User, Segment, UserSegment
from segments.serializers import UserSerializer, SegmentSerializer, UserSegmentSerializer
from segments.services.segment_service import (
    create_segment, update_segment, delete_segment,
    add_user_to_segment, remove_user_from_segment,
    assign_segment_to_random_percent_of_users
)

# Сериализаторы для экшенов
class AddUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(label="ID пользователя")

class RemoveUserSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(label="ID пользователя")

class AssignRandomPercentSerializer(serializers.Serializer):
    percent = serializers.FloatField(label="Процент пользователей")

# Create your views here.

class SegmentViewSet(viewsets.ModelViewSet):
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer

    def create(self, request, *args, **kwargs):
        name = request.data.get("name")
        description = request.data.get("description", "")
        segment = create_segment(name, description)
        serializer = self.get_serializer(segment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        segment = self.get_object()
        name = request.data.get("name")
        description = request.data.get("description")
        updated_segment = update_segment(segment.id, name, description)
        serializer = self.get_serializer(updated_segment)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        segment = self.get_object()
        delete_segment(segment.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def add_user(self, request, pk=None):
        serializer = AddUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        user_segment = add_user_to_segment(user_id, pk)
        return Response(UserSegmentSerializer(user_segment).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def remove_user(self, request, pk=None):
        serializer = RemoveUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data["user_id"]
        remove_user_from_segment(user_id, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"])
    def assign_random_percent(self, request, pk=None):
        serializer = AssignRandomPercentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        percent = serializer.validated_data["percent"]
        count = assign_segment_to_random_percent_of_users(pk, percent)
        return Response({"assigned_count": count})

    def get_serializer_class(self):
        if self.action == 'add_user':
            return AddUserSerializer
        if self.action == 'remove_user':
            return RemoveUserSerializer
        if self.action == 'assign_random_percent':
            return AssignRandomPercentSerializer
        return super().get_serializer_class()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def segments(self, request, pk=None):
        user = self.get_object()
        segments = Segment.objects.filter(user_segments__user=user)
        serializer = SegmentSerializer(segments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="create_user")
    def create_user(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(id=serializer.validated_data["id"])
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
