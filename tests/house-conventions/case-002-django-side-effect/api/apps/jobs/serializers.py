from rest_framework import serializers

from .models import JobPost


class JobPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPost
        fields = ["id", "title", "status", "closed_at"]
