from requests.auth import AuthBase


class NewsApiAuth(AuthBase):

    def __init__(self, api_key: str):
        self.api_key = api_key

    def __call__(self, request):
        request.headers.update(get_auth_headers(self.api_key))
        return request


def get_auth_headers(api_key: str) -> dict:
    return {
        'Content-Type': 'Application/JSON',
        'Authorization': api_key
    }