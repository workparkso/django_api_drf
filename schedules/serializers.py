from rest_framework import serializers
from .models import Schedule

class ScheduleListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) 

    class Meta:
        model = Schedule
        fields = ['id', 'user', 'title', 'select_date', 'time', 'pinned']