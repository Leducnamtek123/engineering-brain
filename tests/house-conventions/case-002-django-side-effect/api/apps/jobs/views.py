from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import JobPost, JobPostActivity
from .permissions import IsCompanyMember
from .serializers import JobPostSerializer
from .services import close_job_post
from .tasks import notify_followers


class JobPostViewSet(viewsets.ModelViewSet):
    serializer_class = JobPostSerializer
    permission_classes = [IsCompanyMember]

    def get_queryset(self):
        return JobPost.objects.filter(company=self.request.user.company).select_related("company")

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        job = close_job_post(self.get_object(), request.user)
        return Response(JobPostSerializer(job).data)

    # Legacy: written before the service layer existed, to be migrated.
    @action(detail=True, methods=["post"])
    def boost(self, request, pk=None):
        job = self.get_object()
        job.title = job.title.strip()
        job.save()
        JobPostActivity.objects.create(job_post=job, actor=request.user, action="boosted")
        notify_followers.delay(job.id, "boosted")
        return Response(JobPostSerializer(job).data, status=status.HTTP_200_OK)
