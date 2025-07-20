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

    path('jobseeker/applications/', views.MyApplicationsView.as_view(), name='my-applications'),
    path('employer/applications/', views.EmployerApplicationUpdateView.as_view(), name='employer-applications'),
    path('employer/applications/<int:pk>/', views.EmployerApplicationUpdateView.as_view(), name='update-application-status'),
    path('company/<int:company_id>/reviews/', views.CompanyReviewView.as_view(), name='company-reviews'),
    path('company/reviews/', views.CompanyReviewView.as_view(), name='company-reviews'),
    path('company/myreviews/',views.CompanyReviewEmployer.as_view(),name="Companys-Review"),
    path('employer/company/', views.CompanyProfileView.as_view(), name='company-profile'),
    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('company/reviews/search/', views.CompanyReviewBySearch.as_view(), name='company-review-search'),
    path('auth/forgot-password/', views.ForgotPasswordView.as_view(), name='forgot-password'),
    path('auth/reset-password/', views.ResetPasswordView.as_view(), name='reset-password'),

    #Followers
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
    path('followers/<int:user_id>/', views.FollowersListView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', views.FollowingListView.as_view(), name='following-list'),

]

