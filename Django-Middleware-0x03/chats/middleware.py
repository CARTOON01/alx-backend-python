from datetime import datetime
import logging
import time
import traceback

# Configure the logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization
        logger.info("RequestLoggingMiddleware initialized")
        
    def __call__(self, request):
        # Code to be executed for each request before the view is called
        start_time = time.time()
        
        # Get the current user
        user = request.user.username if request.user.is_authenticated else "AnonymousUser"
        
        # Log the request with timestamp, user, and path
        logger.info(f"Request started - User: {user} - Method: {request.method} - Path: {request.path}")
        
        try:
            # Process the request
            response = self.get_response(request)
            
            # Code to be executed for each request/response after the view is called
            duration = time.time() - start_time
            logger.info(f"Request completed - User: {user} - Path: {request.path} - Status: {response.status_code} - Duration: {duration:.2f}s")
            
            return response
        except Exception as e:
            logger.error(f"Request failed - User: {user} - Path: {request.path} - Error: {str(e)}")
            logger.error(traceback.format_exc())
            raise
