from django.urls import path
from JobsApp import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns=[
    path('signup/',views.SignupView.as_view(),name="signup"),
    path('login/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',views.LogoutView.as_view(),name="logout"),


    path('jobseeker/profile/', views.JobseekerAPIView.as_view(), name='jobseeker-profile'),
    path('employer/profile/', views.EmployerAPIView.as_view(), name='employer-profile'),

    # For Jobs CRUD
    path('employer/jobs/', views.JobView.as_view()),
    path('employer/jobs/<int:jid>/', views.JobView.as_view()),

    path('jobs/', views.PublicJobListView.as_view(), name='publicjoblist'),
    path('jobs/<int:jid>/', views.JobDetailView.as_view(), name='jobdetail'),

    path('jobs/<int:job_id>/apply/', views.ApplyJobView.as_view(), name='apply-job'),
    path('saved-jobs/', views.SavedJobView.as_view(), name='saved-job-list'),
    path('saved-jobs/<int:jid>/', views.SavedJobView.as_view(), name='save-job'),


]