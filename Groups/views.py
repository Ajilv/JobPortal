from django.shortcuts import render, get_object_or_404
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Group, GroupEvent, GroupJoinRequest
from .serializers import GroupSerializer, GroupEventSerializer, GroupJoinRequestSerializer

# Create your views here.

class GroupListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = GroupSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            group=serializer.save(created_by=request.user)
            group.participants.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        group_id = request.query_params.get("group_id")
        if not group_id:
            return Response({"error": "Enter A valid Group ID"}, status=status.HTTP_400_BAD_REQUEST)

        group = get_object_or_404(Group, id=group_id)
        if group.created_by != request.user:
            return Response({"error": "You do not have permission to delete this group."},
                            status=status.HTTP_403_FORBIDDEN)
        group.delete()
        return Response({"message": "Group deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class GroupEventCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,group_id):
        events = GroupEvent.objects.filter(group_id=group_id)
        serializer=GroupEventSerializer(events,many=True)
        return Response(serializer.data)


    def post(self, request,group_id):
        data = request.data.copy()
        data['created_by'] = request.user.id
        data['group'] = group_id
        group = get_object_or_404(Group, id=group_id)

        is_participant = group.participants.filter(id=request.user.id).exists()

        if not is_participant:
            return Response(
                {"detail": "You must be a participant of this group to create an event."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = GroupEventSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupJoinRequestCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        group_id = request.query_params.get("group_id")
        user_id = request.query_params.get("user_id")
        events = GroupEvent.objects.all()

        if group_id:
            events = events.filter(group_id=group_id)

        if user_id:
            events = events.filter(created_by__id=user_id)

        serializer = GroupEventSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        message = data.get('message')
        group_id = data.get('group')
        group_name = data.get('group_name')

        group = None
        if group_id:
            group = Group.objects.filter(id=group_id).first()
        elif group_name:
            group = Group.objects.filter(Gname=group_name).first()

        if not group:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        if group.created_by == request.user:
            return Response({"error": "You cannot  join your own group."},
                            status=status.HTTP_400_BAD_REQUEST)

        join_request_data = {
            "user": request.user.id,
            "group": group.id,
            "message": message,
        }

        serializer = GroupJoinRequestSerializer(data=join_request_data)
        if serializer.is_valid():
            serializer.save(user=request.user, group=group)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class GroupJoinRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        if group.created_by != request.user:
            return Response({'detail': 'You are not the group owner.'}, status=status.HTTP_403_FORBIDDEN)
        join_requests = GroupJoinRequest.objects.filter(group=group)
        serializer = GroupJoinRequestSerializer(join_requests, many=True)
        return Response(serializer.data)



class HandleJoinRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, join_request_id):
        try:
            join_request = GroupJoinRequest.objects.get(id=join_request_id)
        except GroupJoinRequest.DoesNotExist:
            return Response({"detail": "Join request not found."}, status=status.HTTP_404_NOT_FOUND)

        if join_request.group.created_by != request.user:
            return Response({"detail": "Not authorized.Not the creator"}, status=status.HTTP_403_FORBIDDEN)

        action = request.data.get("action")
        if action == "accept":
            join_request.status = "accepted"
            join_request.group.participants.add(join_request.user)
        elif action == "reject":
            join_request.status = "rejected"
        else:
            return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        join_request.save()
        return Response({"status": join_request.status})



class MyFollowedGroupsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        groups = request.user.followed_groups.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)



class FollowGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        user = request.user


        if group.created_by==request.user:
            return Response({"message":"You Created this group ..."})
        if group.followers.filter(id=user.id).exists():
            return Response({"detail": "You are already following this group."}, status=HTTP_400_BAD_REQUEST)

        group.followers.add(user)
        return Response({"detail": "Followed successfully."})


class UnfollowGroupView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, group_id):
        group = get_object_or_404(Group, id=group_id)
        user = request.user

        if not group.followers.filter(id=user.id).exists():
            return Response({"detail": "You are not following this group."}, status=HTTP_400_BAD_REQUEST)

        group.followers.remove(user)
        return Response({"detail": "Unfollowed successfully."})
