# flashcards/middleware.py
from datetime import datetime
from django.utils.timezone import now

class TelemetryMiddleware:
    """
    Middleware to log telemetry for AI recommendations.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            # Log user interaction (e.g., time and endpoint)
            with open('telemetry.log', 'a') as log_file:
                log_file.write(f"{datetime.now()} - {request.user.username} accessed {request.path}\n")
        return response
