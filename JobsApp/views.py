from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer,JobseekerSerializer,EmployerSerializer,JobModelSerializer,ApplicationSerializer,SavedJobSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from JobsApp.models import Jobseeker,Employer,JobModel,Application,SavedJob

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

class PublicJobListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        jobs = JobModel.objects.filter(isActive=True, employer__is_deleted=False)
        serializer = JobModelSerializer(jobs, many=True)
        return Response(serializer.data)

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
    permission_classes = [IsAuthenticated]

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
            serializer.save(user=user, job=job, resume=seeker_profile.resume)
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