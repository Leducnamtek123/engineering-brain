import unittest

from candidates import Account, Candidate, list_candidates

DATA = [
    Candidate(1, 10, "Nguyễn Văn An", "an@mail.vn", "0912345678", "https://cdn/cv/1.pdf", "applied"),
    Candidate(2, 20, "Trần Thị Bình", "binh@mail.vn", "0987654321", "https://cdn/cv/2.pdf", "offered"),
]


class ListCandidatesTest(unittest.TestCase):
    def test_recruiter_sees_own_company(self):
        self.assertEqual([c.id for c in list_candidates(Account(1, "recruiter", 10), DATA)], [1])

    def test_admin_sees_all(self):
        self.assertEqual(len(list_candidates(Account(2, "admin", None), DATA)), 2)


if __name__ == "__main__":
    unittest.main()
