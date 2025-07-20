from django.urls import path
from Groups.views import GroupListCreateView,GroupJoinRequestsView,GroupEventCreateView,GroupJoinRequestCreateView,HandleJoinRequestView,MyFollowedGroupsView,FollowGroupView,UnfollowGroupView

urlpatterns=[
    path('groups/', GroupListCreateView.as_view()),
    path('groups/join-requests/<int:group_id>/', GroupJoinRequestsView.as_view()),
    path('groups/events/<int:group_id>/', GroupEventCreateView.as_view()),
    path('groups/join-request/', GroupJoinRequestCreateView.as_view()),
    path('groups/join-request/<int:join_request_id>/handle/', HandleJoinRequestView.as_view()),
    path('followed-groups/', MyFollowedGroupsView.as_view(), name='my-followed-groups'),
    path('follow/<int:group_id>/', FollowGroupView.as_view(), name='follow-group'),
    path('unfollow/<int:group_id>/', UnfollowGroupView.as_view(), name='unfollow-group'),
]