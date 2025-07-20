from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Group(models.Model):
    Gname = models.CharField("Group Name", max_length=80,null=True)
    Desc = models.TextField("Description", max_length=300,  blank=True,null=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to="group_profile_pics/", null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='joined_groups', blank=True)
    followers = models.ManyToManyField(User, related_name='followed_groups', blank=True)

    def number_of_participants(self):
        return self.participants.count()

    def number_of_followers(self):
        return self.followers.count()

    def __str__(self):
        return self.Gname or "Unnamed Group"



class GroupJoinRequest(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="join_requests")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.user} -> {self.group} ({self.status})"
    class Meta:
        unique_together=('group','user')



class GroupEvent(models.Model):
    EVENT_TYPES = (
        ('webinar', 'Webinar'),
        ('meetup', 'Meetup'),
        ('post', 'Post'),
        ('job', 'Job Post'),  # Add job post as event type
    )
    profile_pic = models.ImageField(upload_to="Event_Img/", null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    event_datetime = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_events")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title