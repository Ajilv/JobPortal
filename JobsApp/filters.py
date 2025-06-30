import django_filters
from JobsApp.models import JobModel


class JobFilter(django_filters.FilterSet):
    salary_min = django_filters.NumberFilter(field_name='salary', lookup_expr='gte')
    salary_max = django_filters.NumberFilter(field_name='salary', lookup_expr='lte')

    job_type = django_filters.CharFilter(field_name='job_type', lookup_expr='iexact')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')

    class Meta:
        model = JobModel
        fields = ['job_type', 'location', 'salary_min', 'salary_max', 'title']

