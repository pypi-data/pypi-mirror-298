from enum import Enum
from http import HTTPStatus
import traceback
from typing import Dict
import uuid
from django.http import HttpRequest, HttpResponse


STATUS_CODES_MAP = {status.value: status.phrase for status in HTTPStatus}

class ExceptionLogData:
  def __init__(self,exception: Exception, request: HttpRequest):
    self.url = request.get_full_path(force_append_slash=True)
    self.status_code = 500
    self.method = request.method
    self.exception = exception
    self.traceback = traceback.format_exc()
  def get_log_data(self)->Dict:
    log_data = {
        "url":self.url,
        "status_code": self.status_code,
        "method":self.method,
        "exception": str(self.exception),
        "traceback": str(self.traceback),
        "is_automatic_log": True
    }
    return log_data


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class InfoLogData:
  def __init__(self, request: HttpRequest, log_info:Dict ,log_level : LogLevel):
    self.url = request.get_full_path(force_append_slash=True)
    self.method = request.method
    self.log_info= log_info
    if not hasattr(request,'open_observe_id'):
      open_observe_id = str(uuid.uuid4())
      request.open_observe_id = open_observe_id
    self.open_observe_id = request.open_observe_id
    self.tag = log_level

  def get_log_data(self)->Dict:
    log_data = {
        "url":self.url,
        "method":self.method,
        "log_level": self.tag._value_,
        "open_observe_request_id": self.open_observe_id,
        "info": self.log_info,
        "is_automatic_log": False,
    }

    return log_data


class ResponseLogData:
  def __init__(self, request: HttpRequest, response: HttpResponse, duration_ms: float):
    self.url = request.get_full_path(force_append_slash=True)
    self.method = request.method
    self.status_code = response.status_code
    self.duration_in_ms = duration_ms
    self.error_message = None

    if response.status_code >400 and response.status_code < 599 : #if status is client error or server error then log the error message
      response_body = None
      content_type = response.headers.get('Content-Type', '')
      #Add body to log if it's not html 
      if 'text/html'  in content_type:
          response_body = "Body is HTML, not logged to optimize resources"
      else:
          try:
            response_body = response.content.decode('utf-8')
          except UnicodeDecodeError:
            response_body = "<binary data>"
      self.error_message = response_body
  def get_log_data(self)->Dict:
    log_data = {
        "method": self.method,
        "url": self.url,
        "status_code": self.status_code,
        "duration_in_ms": self.duration_in_ms,
        "status_code_words": STATUS_CODES_MAP.get(self.status_code),
        "error_message": self.error_message,
        "is_automatic_log": True
    }
    return log_data