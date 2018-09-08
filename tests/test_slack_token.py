from unittest.mock import Mock, MagicMock, patch
from slack.token import Token

success_mock_token = { 'access_token': 'gooblygook', 'user_id': 'ABC123'}

@patch('slack.token.requests')
def test_generate_token(mocked_request):
    # Setup
    mocked_response = Mock(status_code=200)
    mocked_response.json.return_value = success_mock_token
    mocked_request.get.return_value = mocked_response

    # when
    t = Token(auth_code='123', redirect_uri='http://example.com/auth', client_id='testid', client_secret='testsecret')
    result = t.generate_token()
    expected = {
        "code": '123',
        "redirect_uri": 'http://example.com/auth',
        'client_id': 'testid',
        'client_secret': 'testsecret'
    }

    # then
    mocked_request.get.assert_called_once_with('https://slack.com/api/oauth.access', params=expected)
    mocked_response.json.assert_called_once_with()
    assert result == success_mock_token

@patch('slack.token.requests')
def test_generate_token_unauthorized(mocked_request):
    mocked_response = Mock(status_code=401)
    # mocked_response.json.return_value = None
    mocked_request.get.return_value = mocked_response

    t = Token(auth_code='123', redirect_uri='http://example.com/auth', client_id='testid', client_secret='testsecret')
    result = t.generate_token()
    expected = {
        "code": '123',
        "redirect_uri": 'http://example.com/auth',
        'client_id': 'testid',
        'client_secret': 'testsecret'
    }

    mocked_request.get.assert_called_once_with('https://slack.com/api/oauth.access', params=expected)
    assert result == None
