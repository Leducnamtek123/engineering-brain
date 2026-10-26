from dataclasses import dataclass, field


class EmailTaken(Exception):
    pass


@dataclass
class User:
    id: int
    email: str
    name: str


@dataclass
class JobPost:
    id: int
    owner_id: int
    title: str


@dataclass
class Store:
    users: dict[int, User] = field(default_factory=dict)
    jobs: dict[int, JobPost] = field(default_factory=dict)
    _next_id: int = 1

    def register(self, email: str, name: str) -> User:
        email = email.strip().lower()
        if any(u.email == email for u in self.users.values()):
            raise EmailTaken(email)
        user = User(self._next_id, email, name)
        self.users[user.id] = user
        self._next_id += 1
        return user

    def find_by_email(self, email: str) -> User | None:
        email = email.strip().lower()
        return next((u for u in self.users.values() if u.email == email), None)

    def post_job(self, owner_id: int, title: str) -> JobPost:
        job = JobPost(len(self.jobs) + 1, owner_id, title)
        self.jobs[job.id] = job
        return job

    def public_jobs(self) -> list[JobPost]:
        return list(self.jobs.values())
