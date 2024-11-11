from django.utils.deprecation import MiddlewareMixin


class AddAuthorizationHeaderMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.session.get("access_token")
        if access_token and "HTTP_AUTHORIZATION" not in request.META:
            request.META["HTTP_AUTHORIZATION"] = f"Bearer {access_token}"
