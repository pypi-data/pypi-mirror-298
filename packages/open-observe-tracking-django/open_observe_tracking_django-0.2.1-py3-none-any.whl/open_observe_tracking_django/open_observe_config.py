class OpenObserveConfig:

    def _clean_string(self,value: str) -> str:
      """
      Removes start and ending whitespace and start and ending '/'
      """
      if value is None:
          raise ValueError("The parameter cannot be null.")
      cleaned_value = value.strip().strip('/')
      if not cleaned_value:
          raise ValueError("The parameter cannot be empty after trimming.")
      return cleaned_value

    def __init__(
        self, 
        open_observe_host: str, 
        username: str, 
        password: str, 
        open_observe_organization_name: str, 
        open_observe_stream_name: str
    ) -> None:
        # Validate parameters
        if not open_observe_host:
            raise ValueError("The 'open_observe_host' parameter cannot be null or empty.")
        if not username:
            raise ValueError("The 'username' parameter cannot be null or empty.")
        if not password:
            raise ValueError("The 'password' parameter cannot be null or empty.")
        if not open_observe_organization_name:
            raise ValueError("The 'open_observe_organization_name' parameter cannot be null or empty.")
        if not open_observe_stream_name:
            raise ValueError("The 'open_observe_stream_name' parameter cannot be null or empty.")
        
        # Store parameters
        self.open_observe_host = self._clean_string(open_observe_host)
        self.username = self._clean_string(username)
        self.password = self._clean_string(password)
        self.open_observe_organization_name = self._clean_string(open_observe_organization_name)
        self.open_observe_stream_name = self._clean_string(open_observe_stream_name)

    #function to print the config
    def __repr__(self) -> str:
        return (f"OpenObserveConfig("
                f"open_observe_host='{self.open_observe_host}', "
                f"username='{self.username}', "
                f"password='{self.password}', "
                f"open_observe_organization_name='{self.open_observe_organization_name}', "
                f"open_observe_stream_name='{self.open_observe_stream_name}')")

