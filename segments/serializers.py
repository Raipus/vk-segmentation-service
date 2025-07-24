from rest_framework import serializers
from rest_framework.reverse import reverse
from segments.models import User, Segment, UserSegment

class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "url"]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('user-detail', args=[obj.id], request=request)

class SegmentSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Segment
        fields = ["id", "name", "description", "created_at", "updated_at", "url"]

    def get_url(self, obj):
        request = self.context.get('request')
        return reverse('segment-detail', args=[obj.id], request=request)

class UserSegmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    segment = SegmentSerializer(read_only=True)

    class Meta:
        model = UserSegment
        fields = ["id", "user", "segment", "assigned_at"] 