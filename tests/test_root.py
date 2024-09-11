import pytest


def request_tests():
    return {
        ("en", "2ml"): {
            "magnitude": 2,
            "units": "ml",
        },
        ("en", "2 kCal"): {
            "magnitude": 2,
            "units": "cal",  # TODO: is there a clearer way to represent calorie units? https://en.wikipedia.org/wiki/Calorie  # noqa
        },
    }.items()


@pytest.mark.parametrize("context, expected", request_tests())
def test_request(client, context, expected):
    language_code, description = context
    response = client.post(
        "/",
        data={
            "language_code": language_code,
            "descriptions[]": description,
        },
    )
    result = response.json

    assert expected in result
