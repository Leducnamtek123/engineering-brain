import unittest

from users import EmailTaken, Store


class UsersTest(unittest.TestCase):
    def test_register_and_find(self):
        s = Store()
        u = s.register("An@Example.com", "An")
        self.assertEqual(s.find_by_email("an@example.com").id, u.id)

    def test_email_unique(self):
        s = Store()
        s.register("an@example.com", "An")
        with self.assertRaises(EmailTaken):
            s.register("AN@example.com", "An 2")

    def test_public_jobs(self):
        s = Store()
        u = s.register("hr@acme.vn", "HR")
        s.post_job(u.id, "Backend Engineer")
        self.assertEqual(len(s.public_jobs()), 1)


if __name__ == "__main__":
    unittest.main()
