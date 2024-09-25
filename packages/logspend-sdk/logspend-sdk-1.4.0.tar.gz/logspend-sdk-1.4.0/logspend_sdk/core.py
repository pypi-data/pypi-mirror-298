import time
import uuid
import threading
import queue
import httpx
import logging
import atexit

from logspend_sdk.constants import SDK_VERSION

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class LogBuilder:
    def __init__(self, input_data):
        """
        Initializes a new instance of LogBuilder.

        :param input_data: dict - A dictionary containing the initial input data for the LLM call log, e.g. prompt, model and model parameters like temperature, max_tokens.
        """
        self.data = {
            "input": input_data,
            "output": {},
            "identity": {},
            "custom_properties": {},
            "start_time_ms": int(time.time() * 1000),
            "end_time_ms": 0,
            "latency_ms": 0,
            "request_id": str(uuid.uuid4()),
        }

    def set_output(self, output_data):
        """
        Sets the output data from the LLM generation call.

        :param output_data: dict - A dictionary containing the output data of the LLM log, this includes the generated text.
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        if not self.data["output"]:
            self.data["output"] = output_data
            if not self.data["end_time_ms"]:
                self.data["end_time_ms"] = int(time.time() * 1000)
        return self
    
    def set_identity(self, identity_dict):
        """
        Sets the identity information for the log. It contains a session_id and a user_id to identify the user.

        :param identity_dict: dict - A dictionary with identity fields including session_id and user_id.
        """
        # Add identity to self.data; session_id and user_id are optional and will be included if present
        if identity_dict:
            self.data["identity"] = identity_dict
        return self

    def set_custom_properties(self, custom_properties_data):
        """
        Sets custom properties for the LLM log. This could be a user_id, generation_id, session_id, etc.

        :param custom_properties_data: dict - A dictionary containing custom properties to be added to the log.
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        if custom_properties_data:
            self.data["custom_properties"] = custom_properties_data
        return self
    
    def set_start_time(self, start_time):
        """
        Sets the start time of the log event, representing when the LLM call request was made.
        This is used to estimate the latency.

        :param start_time: float - A floating-point number representing the start time. 
                                  This should be a timestamp in seconds since the epoch (as returned by time.time()).
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["start_time_ms"] = int(start_time * 1000)
        return self
    
    def set_end_time(self, end_time):
        """
        Sets the end time of the log event, representing when the LLM call response was received from the server.
        This is used to estimate the latency.

        :param end_time: float - A floating-point number representing the end time. 
                                This should be a timestamp in seconds since the epoch (as returned by time.time()).
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["end_time_ms"] = int(end_time * 1000)
        return self
    
    def set_latency(self, latency):
        """
        Sets the latency in milliseconds, representing the elapsed time between the start time (when the LLM request was made)
        and the end time (when the LLM response was received from the server).
        Example: 
        start_time = time.time()
        # Make LLM call ...
        end_time = time.time()
        latency = end_time - start_time

        :param latency: float - A floating-point number representing the difference between the end time and start time. 
                                This should be a timestamp in seconds since the epoch (as returned by time.time()).
        :return: LogBuilder - The instance of LogBuilder for method chaining.
        """
        self.data["latency_ms"] = int(latency * 1000)
        return self

    def build(self):
        """
        Finalizes and returns the constructed log data.

        :return: dict - A dictionary containing the structured log data.
        """
        return self.data


class LogSpendLogger:
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, api_key, project_id, api_url="https://api.log.com/llm/v1/log", integration_type=None, async_mode=True):
        # Create a unique key based on constructor arguments so we have a Singleton object for each combination
        key = (api_key, project_id, api_url, integration_type, async_mode)

        with cls._lock:
            if key not in cls._instances:
                instance = super(LogSpendLogger, cls).__new__(cls)
                cls._instances[key] = instance
        return cls._instances[key]
    
    def __init__(self, api_key, project_id, api_url="https://api.logspend.com/llm/v1/log", integration_type=None, async_mode=True):
        # Ensure the instance is initialized with arguments
        key = (api_key, project_id, api_url, integration_type, async_mode)
        if not hasattr(self, '_initialized_for'):
            self.api_key = api_key
            self.project_id = project_id
            self.api_url = api_url
            self.sdk_version = SDK_VERSION if not integration_type else f"{integration_type}:{SDK_VERSION}"
            self.async_mode = async_mode
            self._queue = queue.Queue()
            self._stop_event = threading.Event()
            self._thread = threading.Thread(target=self._process_queue, daemon=True)
            self._thread.start()

            # Register atexit handler to stop the thread when the program exits
            atexit.register(self.close)
            
            # Mark the instance as initialized for this specific combination of arguments
            self._initialized_for = key
    
    def send(self, data):
        if not self.async_mode:
            self._send_request(data)
            return
        # Add the data to the queue
        self._queue.put(data)
        
    def _process_queue(self):
        while not self._stop_event.is_set():
            try:
                data = self._queue.get(timeout=0.5)  # Wait for 500 ms for an item to be available
                if data is None:  # Sentinel to shut down the thread
                    break
                
                # Perform the HTTP post in this thread
                self._send_request(data)
            except queue.Empty:
                continue  # Continue to check for more items or stop event
                    
    def _send_request(self, data):
        # Check if input and output are properly set
        if not data.get("input") or not data.get("output"):
            error_msg = "Input or Output data missing. Will skip sending LLM log to LogSpend."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "LogSpend-SDK-Version": self.sdk_version,
            "LogSpend-Project-ID": self.project_id,
            "LogSpend-Request-ID": data["request_id"]
        }

        timeout_duration = 0.5  # max timeout 500 milliseconds
        with httpx.Client() as client:
            try:
                response = client.post(self.api_url, headers=headers, json=data, timeout=timeout_duration)
                # Check if the request was unauthorized due to issue with the API key
                if response.status_code == 401:
                    try:
                        # Extract the error message from the response
                        error_data = response.json()
                        error_msg = error_data.get("message", "Unauthorized access")
                    except ValueError:
                        # In case the response isn't a JSON, use default message
                        error_msg = "Unauthorized access"
                        
                    logger.error(f"{response.status_code} Unauthorized: {error_msg}")
                    raise PermissionError(error_msg)
            
                # Check if the request was successful
                if response.is_success:
                    response_data = response.json()
                    return response_data["data"]["request_id"]
                else:
                    logger.error(f"HTTP Error when sending LLM log to LogSpend: {response.status_code}")
                    return None
            except PermissionError:
                raise
            except Exception as e:
                logger.error(f"Error sending LLM log to LogSpend: {e}")
                return None
            
    def close(self):
        # Signal the thread to stop and wait for it to finish
        if self._thread.is_alive():
            self._stop_event.set()
            self._queue.put(None)  # Sentinel to ensure the thread exits
            self._thread.join()