from datetime import datetime
import logging

# Configure the logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get the current user
        user = request.user
        
        # Log the request with timestamp, user, and path
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        # Process the request
        response = self.get_response(request)
        
        return response
