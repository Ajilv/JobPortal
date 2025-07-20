from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer,JobseekerSerializer,EmployerSerializer,JobModelSerializer,ApplicationSerializer,SavedJobSerializer,CompanySerializer,CompanyReviewSerializer,ResetPasswordSerializer,ForgotPasswordSerializer,UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from JobsApp.models import Jobseeker,Employer,JobModel,Application,SavedJob,Company,CompanyReview,PasswordResetOTP,Follower
from JobsApp.permissions import IsEmployer,IsSeeker
from rest_framework import generics,filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import JobFilter
from JobsApp.utility import generate_otp

User = get_user_model()

class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class JobseekerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Jobseeker.objects.get(name=request.user, is_deleted=False)
            serializer = JobseekerSerializer(profile)
            return Response(serializer.data)
        except Jobseeker.DoesNotExist:
            return Response({"error": "Profile is not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if request.user.type != "Seeker":
            return Response({"error": "Only jobseekers can create a jobseeker profile."}, status=403)
        serializer = JobseekerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(name=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            jobseeker = Jobseeker.objects.get(name=request.user, is_deleted=False)
        except Jobseeker.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobseekerSerializer(jobseeker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            jobseeker = Jobseeker.objects.get(name=request.user, is_deleted=False)
            jobseeker.is_deleted = True
            jobseeker.save()
            return Response({'message': 'Profile soft-deleted'}, status=status.HTTP_200_OK)
        except Jobseeker.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class EmployerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = Employer.objects.get(user=request.user, is_deleted=False)
            serializer = EmployerSerializer(profile)
            return Response(serializer.data)
        except Employer.DoesNotExist:
            return Response({"error": "Profile is not There"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if Employer.objects.filter(user=request.user, is_deleted=False).exists():
            return Response({'error': 'Employer profile already exists'}, status=400)

        serializer = EmployerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        try:
            employer = Employer.objects.get(user=request.user, is_deleted=False)
        except Employer.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployerSerializer(employer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            employer = Employer.objects.get(user=request.user, is_deleted=False)
            employer.is_deleted = True
            employer.save()
            return Response({'message': 'Profile soft-deleted'}, status=status.HTTP_200_OK)
        except Employer.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

class JobView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        jobs= JobModel.objects.filter(employer__user=request.user,isActive=True,employer__is_deleted=False)
        job_type = request.GET.get('job_type')
        location = request.GET.get('location')

        if job_type:
            jobs = jobs.filter(job_type__iexact=job_type)
        if location:
            jobs = jobs.filter(location__icontains=location)

        serializer=JobModelSerializer(jobs,many=True)
        return Response(serializer.data)

    def post(self,request):
        try:
            employer = Employer.objects.get(user=request.user, is_deleted=False)
        except Employer.DoesNotExist:
            return Response({'error': 'Employer not found'}, status=404)
        serializer=JobModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=employer)
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

    def put(self,request,jid):
        try:
            job=JobModel.objects.get(id=jid,employer__user=request.user)
        except JobModel.DoesNotExist:
            return Response({'error':'Job Not Found'},status=404)
        serializer=JobModelSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'Message':'Data updated '},status=200)
        return Response(serializer.errors,status=400)

    def delete(self, request, jid):
        try:
            job = JobModel.objects.get(id=jid, employer__user=request.user)
        except JobModel.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)

        job.isActive = False
        job.save()
        return Response({'message': 'Job soft deleted'}, status=200)

class PublicJobListView(generics.ListAPIView):
    queryset = JobModel.objects.filter(isActive=True, employer__is_deleted=False)
    serializer_class = JobModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = JobFilter
    search_fields = ['title', 'desciption']



class JobDetailView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, jid):
        try:
            job = JobModel.objects.get(id=jid, isActive=True, employer__is_deleted=False)
            serializer = JobModelSerializer(job)
            return Response(serializer.data)
        except JobModel.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)




class ApplyJobView(APIView):
    permission_classes = [IsAuthenticated,IsSeeker]

    def post(self, request, job_id):
        user = request.user
        if user.type != "Seeker":
            return Response({'error': 'Only job seekers can apply.'}, status=403)
        try:
            job = JobModel.objects.get(id=job_id, isActive=True)
        except JobModel.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)

        if Application.objects.filter(user=user, job=job).exists():
            return Response({'error': 'You  already applied to this job.'}, status=400)


        try:
            seeker_profile = user.jobseeker
        except Jobseeker.DoesNotExist:
            return Response({'error': 'Jobseeker profile not found.'}, status=404)

        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, job=job, resume=seeker_profile.resume,profile_pic=seeker_profile.profile_pic)
            return Response({'message': 'Application submitted successfully.'}, status=201)

        return Response(serializer.errors, status=400)

class SavedJobView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'jobseeker'):
            return Response({'error': 'Only jobseekers can view saved jobs'}, status=403)

        saved_jobs = SavedJob.objects.filter(user=request.user)
        serializer = SavedJobSerializer(saved_jobs, many=True)
        return Response(serializer.data)

    def post(self, request, jid):
        if not hasattr(request.user, 'jobseeker'):
            return Response({'error': 'Only jobseekers can save jobs'}, status=403)

        try:
            job = JobModel.objects.get(id=jid, isActive=True)
        except JobModel.DoesNotExist:
            return Response({'error': 'Job not found'}, status=404)

        if SavedJob.objects.filter(user=request.user, job=job).exists():
            return Response({'error': 'Already saved'}, status=400)

        SavedJob.objects.create(user=request.user, job=job)
        return Response({'message': 'Job saved successfully'}, status=201)

    def delete(self, request, jid):
        try:
            saved = SavedJob.objects.get(user=request.user, job__id=jid)
        except SavedJob.DoesNotExist:
            return Response({'error': 'Not saved'}, status=404)

        saved.delete()
        return Response({'message': 'Job unsaved successfully'}, status=200)



class MyApplicationsView(APIView):
    permission_classes = [IsAuthenticated,IsSeeker]

    def get(self, request):
        applications = Application.objects.filter(user=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)


class EmployerApplicationUpdateView(APIView):
    permission_classes = [IsAuthenticated,IsEmployer]

    def get(self, request):
        applications = Application.objects.filter(job__employer__user=request.user)
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        # Update application status
        try:
            application = Application.objects.get(id=pk, job__employer__user=request.user)
        except Application.DoesNotExist:
            return Response({'error': 'Application not found'}, status=404)

        status_val = request.data.get('status')
        if status_val not in ['applied', 'viewed', 'shortlisted', 'rejected']:
            return Response({'error': 'Invalid status'}, status=400)

        application.status = status_val
        application.save()
        return Response({'message': f'Status updated to {status_val}'})



    # search_fields = ['job_title', 'location', 'company__name']
class CompanyProfileView(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        try:
            company = Company.objects.get(employer__user=request.user)
            serializer = CompanySerializer(company)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({'error': 'Company profile not found'}, status=404)

    def post(self, request):
        employer = Employer.objects.get(user=request.user)
        if Company.objects.filter(employer=employer).exists():
            return Response({'error': 'Profile already exists'}, status=400)
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=employer)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request):
        try:
            company = Company.objects.get(employer__user=request.user)
        except Company.DoesNotExist:
            return Response({'error': 'Company profile not found'}, status=404)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CompanyReviewEmployer(APIView):
    permission_classes = [IsAuthenticated, IsEmployer]

    def get(self, request):
        try:
            company = Company.objects.get(employer__user=request.user)
        except Company.DoesNotExist:
            return Response({'error': 'Company profile not found'}, status=404)

        reviews = CompanyReview.objects.filter(company=company)
        serializer = CompanyReviewSerializer(reviews, many=True)
        return Response(serializer.data)



class CompanyReviewView(APIView):
    permission_classes = [IsAuthenticated, IsSeeker]

    def post(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({'error': 'Company not found'}, status=404)

        if CompanyReview.objects.filter(company=company, reviewer=request.user).exists():
            return Response({'error': 'You already reviewed this company'}, status=400)

        serializer = CompanyReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(reviewer=request.user, company=company)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request, company_id=None):
        if company_id:
            reviews = CompanyReview.objects.filter(company_id=company_id)
        else:
            reviews = CompanyReview.objects.all()
        serializer = CompanyReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class CompanyReviewBySearch(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        name = request.GET.get('name')
        company_id = request.GET.get('id')

        # Check if name or ID is provided
        if name:
            companies = Company.objects.filter(name__icontains=name)
        elif company_id:
            companies = Company.objects.filter(id=company_id)
        else:
            return Response({'error': 'Please provide either company name or ID'}, status=400)

        if not companies.exists():
            return Response({'error': 'Company not found'}, status=404)

        reviews = CompanyReview.objects.filter(company__in=companies)
        serializer = CompanyReviewSerializer(reviews, many=True)
        return Response(serializer.data)


User = get_user_model()

class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            otp = generate_otp()

            PasswordResetOTP.objects.create(user=user, otp=otp)

            print(f"OTP for {email}: {otp}")

            return Response({'message': 'OTP sent successfully'})
        return Response(serializer.errors, status=400)

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
                otp_record = PasswordResetOTP.objects.filter(user=user, otp=otp, is_used=False).latest('created_at')

                from datetime import timedelta
                from django.utils import timezone
                if timezone.now() - otp_record.created_at > timedelta(minutes=10):
                    return Response({'error': 'OTP expired'}, status=400)

                user.set_password(new_password)
                user.save()

                otp_record.is_used = True
                otp_record.save()

                return Response({'message': 'Password reset successful'})
            except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
                return Response({'error': 'Invalid OTP or email'}, status=400)
        return Response(serializer.errors, status=400)


class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            to_follow = User.objects.get(id=user_id)
            if request.user == to_follow:
                return Response({"error": "You can't follow yourself"}, status=400)

            follow_obj,created = Follower.objects.get_or_create(follower=request.user, following=to_follow)
            if not created:
                return Response({"message":"The User is alredy followed "})

            return Response({"message": "Followed successfully"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if request.user==to_unfollow:
            return Response({"error":"you cant  unfollow yourself"},status=400)

        follow_ornot=Follower.objects.filter(follower=request.user,following=to_unfollow).first()

        if not follow_ornot:
            return Response({"message":"You need to follow before unfollowing "},status=400)
        follow_ornot.delete()
        return Response({"message":f"You Have successfully Unfollowed the user {to_unfollow.username}"},status=200)

class FollowersListView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            followers = Follower.objects.filter(following=user).values_list('follower', flat=True)
            users = User.objects.filter(id__in=followers)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class FollowingListView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            following = Follower.objects.filter(follower=user).values_list('following', flat=True)
            users = User.objects.filter(id__in=following)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)