import json
from typing import Dict

from celery import shared_task
import requests
from .open_observe_config import OpenObserveConfig
from .logged_classes import (InfoLogData, ExceptionLogData,
ResponseLogData, LogLevel
                             )
from django.http import HttpRequest, HttpResponse


import logging
from requests.auth import HTTPBasicAuth




class OpenObserveSender:
    def __init__(self, config : OpenObserveConfig) -> None:
        self.auth = HTTPBasicAuth(config.username, config.password)  # Store auth credentials
        open_obseve_url = f"{config.open_observe_host}/api/{config.open_observe_organization_name}/{config.open_observe_stream_name}/_json"
        self.open_observe_url = open_obseve_url
        self.logger = logging.getLogger("RequestLogger")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_response(self, request:HttpRequest,response:HttpResponse, duration_in_ms:float ) -> None:
        response_log_data = ResponseLogData(request=request,response=response,duration_ms=duration_in_ms)
        # Send log to external log server
        self.send_log_to_open_observe(response_log_data.get_log_data())

    def log_exception(self, exception: Exception, request: HttpRequest) -> None:
        """
        Log unhandled exceptions.
        
        :param exception: The exception object.
        """
        exception_log = ExceptionLogData(exception=exception, request=request)
        # Send log to external log server
        self.send_log_to_open_observe(exception_log.get_log_data())

    def send_log_to_open_observe(self, log_data: dict) -> None:
        """
        Private method to send log data to a remote server.
        
        :param log_data: Log data in JSON format.
        """
        send_log_async_with_celery.delay( open_observe_url= self.open_observe_url, log_data=log_data, username=self.auth.username, password=self.auth.password)
            

@shared_task
def send_log_async_with_celery(open_observe_url:str,username:str, password:str, log_data:dict):
    try:
        headers = {'Content-Type': 'application/json'}
        auth = HTTPBasicAuth(username=username, password=password)
        r = requests.post(open_observe_url, auth=auth, data=json.dumps(log_data), headers=headers)
        if r.status_code != 200:
          logging.error(f"Failed to send log to server: {r.text}")
        else:
          logging.info(f"Log sent to openobserve")

    except requests.exceptions.RequestException as e:
          logging.error(f"Failed to send log to server: {r.text}")


  
  

