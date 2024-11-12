from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed


class AddAuthorizationHeaderMiddleware(MiddlewareMixin):
    PUBLIC_ENDPOINTS = [
        "/auth/register/",
        "/auth/users/reset_password/",
        "/auth/users/reset_password_confirm/",
        "/auth/login/",
        "/auth/jwt/refresh/",
        "/auth/jwt/verify/",
        "/swagger/",
        "/admin/",
    ]

    def process_request(self, request):
        if any(request.path.startswith(endpoint) for endpoint in self.PUBLIC_ENDPOINTS):
            return

        access_token = request.session.get("access_token")

        if access_token:
            if "HTTP_AUTHORIZATION" not in request.META:
                request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
        else:
            raise AuthenticationFailed("Token is missing")
