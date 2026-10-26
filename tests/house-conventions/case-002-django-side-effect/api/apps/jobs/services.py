from django.db import transaction
from django.utils import timezone

from .models import JobPost, JobPostActivity
from .tasks import notify_followers


def close_job_post(job: JobPost, by_user) -> JobPost:
    """Đóng tin tuyển dụng: ghi nhận người đóng, lưu lịch sử, báo cho người theo dõi sau khi commit."""
    with transaction.atomic():
        job.status = JobPost.STATUS_CLOSED
        job.closed_at = timezone.now()
        job.closed_by = by_user
        job.save(update_fields=["status", "closed_at", "closed_by"])
        JobPostActivity.objects.create(job_post=job, actor=by_user, action="closed")
        transaction.on_commit(lambda: notify_followers.delay(job.id, "closed"))
    return job
