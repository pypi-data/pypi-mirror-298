
from typing import Dict
from django.http import HttpRequest

from open_observe_tracking_django.logged_classes import InfoLogData, LogLevel

from .sender_singletone import setup_open_observe_sender

sender = None
def log_to_open_observe(request:HttpRequest,log_level : LogLevel,info:Dict ):
  """
  Send logs to open observe and to the terminal

  :param request: To identify the request in which the log was sent
  :param log_level: The tag you want to add to the log level
  :param info: A dictionary to be sent to open observe, ("key": value pairs)

  ## Example:

    info = {"user_id": 32323, "user_name": "Than", "message": "Is trying to send messages to blocked user"}
    # Call the logging function
    log_to_open_observe(request, LogLevel.WARNING, info)
    
    # Another
    info = {"error","Database is not responding"}
    # Call the logging function
    log_to_open_observe(request, LogLevel.CRITICAL, info)
  """
  global sender
  if sender == None:
    sender = setup_open_observe_sender()

  log = InfoLogData(request=request,log_info=info,log_level=log_level)
  sender.send_log_to_open_observe(log_data=log.get_log_data())
