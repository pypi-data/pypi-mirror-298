from django.http import HttpResponseNotFound
from django.shortcuts import render

class HandleHTTPErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if the response is a 404
        if response.status_code == 400:
            return self.handle_http_error(request, status_code=response.status_code)

        elif response.status_code == 403:
            return self.handle_http_error(request, status_code=response.status_code)

        elif response.status_code == 404:
            return self.handle_http_error(request, status_code=response.status_code)

        elif response.status_code == 500:
            return self.handle_http_error(request, status_code=response.status_code)
        
        return response

    def handle_http_error(self, request, status_code, message = None):
        # You can customize the response for undefined URLs here
        return render(request, f"pages/states/errors/{status_code}.html", { "message": message}, status=status_code)
