import email.message
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent))
import refresh  # noqa: E402


def http_error(code, retry_after=None):
    headers = email.message.Message()
    if retry_after is not None:
        headers["Retry-After"] = retry_after
    return urllib.error.HTTPError("https://x.test/", code, "x", headers, None)


class Ok:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self):
        return b"{}"


class RetryAfterTest(unittest.TestCase):
    def test_server_value_is_used_and_capped(self):
        self.assertEqual(refresh.retry_after("7", 0), 7)
        self.assertEqual(refresh.retry_after("900", 0), 120)

    def test_backoff_without_a_number(self):
        self.assertEqual(refresh.retry_after(None, 0), 5)
        self.assertEqual(refresh.retry_after("Wed, 21 Oct 2015 07:28:00 GMT", 2), 20)


class HttpTest(unittest.TestCase):
    def test_429_is_retried_until_it_succeeds(self):
        answers = [http_error(429, "1"), http_error(429, "1"), Ok()]

        def fake(req, timeout):
            a = answers.pop(0)
            if isinstance(a, Exception):
                raise a
            return a

        with mock.patch("urllib.request.urlopen", fake), mock.patch("time.sleep") as sleep:
            self.assertEqual(refresh.http("https://x.test/"), (200, b"{}"))
        self.assertEqual([c.args[0] for c in sleep.call_args_list], [1, 1])

    def test_404_is_an_answer(self):
        with mock.patch("urllib.request.urlopen", side_effect=http_error(404)), mock.patch("time.sleep"):
            self.assertEqual(refresh.http("https://x.test/"), (404, b""))

    def test_endless_429_gives_up(self):
        with mock.patch("urllib.request.urlopen", side_effect=http_error(429, "1")), mock.patch("time.sleep"):
            self.assertEqual(refresh.http("https://x.test/")[0], 429)


if __name__ == "__main__":
    unittest.main()
