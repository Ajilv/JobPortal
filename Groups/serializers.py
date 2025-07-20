from rest_framework import serializers
from .models import Group, GroupEvent, GroupJoinRequest
from JobsApp.models import User

class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    participants = serializers.StringRelatedField(read_only=True,many=True)

    participants_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = "__all__"

    def get_participants_count(self, obj):
        return obj.participants.count()


class GroupEventSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(read_only=True)
    group=serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupEvent
        fields = "__all__"

    def validate(self, data):
        user = self.context['request'].user
        if data['event_type'] == 'job' and not user.is_employer:
            raise serializers.ValidationError("Only employers can post job events.")
        return data


class GroupJoinRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = GroupJoinRequest
        fields = "__all__"
