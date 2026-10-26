# Agent rules (backend)

- Django REST Framework. Keep ViewSets thin: permission checks and orchestration only.
- Business logic that writes data lives in `api/apps/<app>/services.py`.
- Multi-table writes are wrapped in `transaction.atomic()`.
- Side effects (Celery tasks, emails, webhooks) are only triggered inside `transaction.on_commit()`.
- Some older views still write directly and call `.delay()` inline; they are being migrated. Do not copy that pattern.
