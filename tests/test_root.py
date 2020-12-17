import pytest


def request_tests():
    return {
        '2ml': {
            'magnitude': 2,
            'units': 'ml',
        },
    }.items()


@pytest.mark.parametrize('description,expected', request_tests())
def test_request(client, description, expected):
    response = client.post('/', data={'descriptions[]': description})
    result = response.json

    assert description in result
    assert result[description] == expected
