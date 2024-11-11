from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve


class AddAuthorizationHeaderMiddleware(MiddlewareMixin):
    PUBLIC_ENDPOINTS = [
        "/auth/register/",
        "/auth/users/reset_password/",
        "/auth/users/reset_password_confirm/",
        "/auth/login/",
        "/auth/jwt/refresh/",
        "/auth/jwt/verify/",
        "/swagger/",
        "/admin",
    ]

    def process_request(self, request):
        if any(request.path.startswith(endpoint) for endpoint in self.PUBLIC_ENDPOINTS):
            return

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            from rest_framework.exceptions import AuthenticationFailed

            raise AuthenticationFailed("Token is missing")
