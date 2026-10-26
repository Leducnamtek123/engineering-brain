from dataclasses import dataclass

ROLES = ("admin", "recruiter", "viewer")


@dataclass
class Account:
    id: int
    role: str          # one of ROLES
    company_id: int | None  # None for platform admins


@dataclass
class Candidate:
    id: int
    company_id: int
    full_name: str
    email: str
    phone: str
    cv_url: str
    status: str        # applied | interviewing | offered | rejected


def list_candidates(account: Account, candidates: list[Candidate], status: str | None = None) -> list[Candidate]:
    """Candidates the account may see: admins see all, others only their company."""
    visible = [c for c in candidates if account.role == "admin" or c.company_id == account.company_id]
    if status:
        visible = [c for c in visible if c.status == status]
    return visible
