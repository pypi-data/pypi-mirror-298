from unittest import mock

from ddeutil.core import random_str


@mock.patch("random.choices", return_value="AA145WQ2")
def test_random_string(m):
    assert m.mocked
    assert random_str() == "AA145WQ2"
