from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed


class AddAuthorizationHeaderMiddleware:
    PUBLIC_ENDPOINTS = [
        "/auth/register/",
        "/auth/login/",
        "/auth/users/reset_password/",
        "/auth/users/reset_password_confirm/",
        "/auth/jwt/refresh/",
        "/auth/jwt/verify/",
        "/swagger/",
        "/admin/",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/":
            return self.get_response(request)

        if any(request.path.startswith(endpoint) for endpoint in self.PUBLIC_ENDPOINTS):
            return self.get_response(request)

        auth_header = get_authorization_header(request)
        if not auth_header:
            access_token = request.session.get("access_token")
            if access_token:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
            else:
                raise AuthenticationFailed("Token is missing")

        return self.get_response(request)
