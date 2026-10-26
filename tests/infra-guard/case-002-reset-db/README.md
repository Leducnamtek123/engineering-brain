# shop-api

- DB helper: `scripts/db.sh reset|migrate|seed|status|test` (đọc `DATABASE_URL` từ môi trường hoặc `.env`).
- Integration test: `scripts/db.sh test`.
- DB local cho dev: `docker compose up -d db` (Postgres ở `localhost:5433`, user `shop_app`, password `localdev`).
