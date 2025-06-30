from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from JobPortal import settings
# Create your models here.

class User(AbstractUser):

    class Types(models.TextChoices):
        Emp = "Employee", "Employee"
        Seeker = "Seeker", "Seeker"

    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(unique = True)
    native_name = models.CharField(max_length = 5)
    phone_no = models.CharField(max_length = 10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    type = models.CharField(
        max_length=20, choices=Types.choices, default=Types.Emp
    )
    def __str__(self):
        return self.username

class Jobseeker(models.Model):
    name= models.OneToOneField(User,on_delete=models.CASCADE)
    resume=models.FileField(upload_to="resumes/",null=True)
    exp=models.CharField(max_length=60,null=True,blank=True)
    skills=models.CharField(max_length=100,null=True,blank=True)
    Education=models.TextField(max_length=200,null=True,blank=True)
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        return f"JobSeeker Name :{self.name}"

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Employer: {self.user.email}"


class JobModel(models.Model):
    Job_Types=(
        ('Full-Time','Full-Time'),
        ('Part-Time','Part-Time'),
        ('Internship','Internship')
    )

    employer = models.ForeignKey(Employer,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    desciption=models.TextField(max_length=200,null=True)
    job_type=models.CharField(max_length=30,choices=Job_Types)
    location=models.CharField(max_length=100,null=True,blank=True)
    salary=models.IntegerField(null=True,blank=True)
    isActive=models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('viewed', 'Viewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey('JobModel', on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='applications/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')


    class Meta:
        unique_together = ('job', 'user')

    def __str__(self):
        return f"{self.user.username} : {self.job.title}"

class SavedJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey('JobModel', on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user} saved {self.job}"


class Company(models.Model):
    employer = models.OneToOneField(Employer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class CompanyReview(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['company', 'reviewer']

    def __str__(self):
        return f"{self.reviewer.username} - {self.company.name} ({self.rating})"
