from django.contrib import admin
from JobsApp import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Jobseeker)
admin.site.register(models.Employer)
admin.site.register(models.JobModel)
admin.site.register(models.Application)
admin.site.register(models.Company)