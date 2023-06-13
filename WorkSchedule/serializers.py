from rest_framework import serializers

from WorkSchedule.models import O_WorkSchedule, S_WorkSchedule, WorkSchedule


class S_WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_WorkSchedule
        fields = ["work_day", "shift", "description"]


class O_WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = O_WorkSchedule
        fields = ''


class WorkScheduleCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=250)
    closing_date = serializers.DateTimeField()

    class Meta:
        model = WorkSchedule
        fields = ["store_id"]

    def validate(self, attrs):
        return attrs


class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = "__all__"


class DaySerializer(serializers.Serializer):
    day = serializers.CharField()


class StaffWorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = S_WorkSchedule
        fields = ["work_day", "shift", "description"]
