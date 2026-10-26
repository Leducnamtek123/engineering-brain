from celery import shared_task


@shared_task
def notify_followers(job_post_id: int, event: str) -> None:
    """Gửi thông báo cho ứng viên đang theo dõi công ty khi tin tuyển dụng đổi trạng thái."""
    ...
