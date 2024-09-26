
import time
from typing import Callable

from django.http import HttpRequest, HttpResponse
from .sender_creator import setup_open_observe_sender


class OpenObserveTrackingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.open_openobserve_sender = setup_open_observe_sender()

    def process_exception(self, request, exception):
        """
        This captures an exception from the self.get_response() inside the __call__ method
        """
        self.open_openobserve_sender.log_exception(exception=exception,request=request)  # Log the exception
        self.had_unhandled_exception=True
        raise exception # re raise exception if you want another middleware to handle the request with custom messages

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        This captures the request before it gets to the view and after the view creates a response
        """
        # Before sending the request to the view
        self.had_unhandled_exception = False
        start_time = time.perf_counter()
        # Process the request and get the response
        response = self.get_response(request)  # Can throw and exception if there was an unhandled exception on the view
        # After the view finish processing
        duration_in_ms = (time.perf_counter()-start_time) *1000
        duration_formatted = round(duration_in_ms, 4)
        print(duration_formatted)
        # If no expection Log the request and response details
        if self.had_unhandled_exception == False:
          self.open_openobserve_sender.log_response(  request=request, response=response,duration_in_ms=duration_formatted)
        return response