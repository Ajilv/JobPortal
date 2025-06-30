from rest_framework import serializers
from .models import User,Jobseeker,Employer,JobModel,Application,SavedJob,Company,CompanyReview
from django.contrib.auth.password_validation import validate_password


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'native_name',
            'phone_no',
            'type',
        ]

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data.get('username'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            native_name=validated_data.get('native_name'),
            phone_no=validated_data.get('phone_no'),
            type=validated_data.get('type'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
class JobseekerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobseeker
        fields = '__all__'
        read_only_fields = ['name']

class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = '__all__'
        read_only_fields = ['user']

class JobModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobModel
        fields = '__all__'
        read_only_fields=['employer']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['id', 'job', 'resume', 'applied_at','user']

class SavedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedJob
        fields = '__all__'
        read_only_fields = ['user', 'saved_at']

class CompanyReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyReview
        fields = '__all__'
        read_only_fields = ['reviewer','company']

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['employer']
