
# The sender has to be setted up with setup_open_observe_sender function
from .open_observe_config import OpenObserveConfig
from .open_observe_sender import OpenObserveSender

from django.conf import settings

def setup_open_observe_sender()->OpenObserveSender:
  config_from_settings = settings.OPENOBSERVE_CONFIG
  config = OpenObserveConfig(
    username=config_from_settings["username"],
    password=config_from_settings["password"],
    open_observe_host=config_from_settings["open_observe_host"],
    open_observe_organization_name=config_from_settings["open_observe_organization_name"],
    open_observe_stream_name=config_from_settings["open_observe_stream_name"],
  )
  new_sender = OpenObserveSender(config=config)
  return new_sender