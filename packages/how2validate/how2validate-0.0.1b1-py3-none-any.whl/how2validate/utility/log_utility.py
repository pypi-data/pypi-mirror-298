# src/python/how2validate/utility/logging_utility.py

import logging
import sys

from how2validate.utility.config_utility import get_active_secret_status, get_inactive_secret_status

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def get_secret_status_message(service, is_active, response=None, response_data=None):
    # Normalize is_active values to handle both 'Active' and 'InActive'
    if is_active == get_active_secret_status():
        status = "active and operational"
    elif is_active == get_inactive_secret_status():
        status = "inactive and not operational"
    else:
        raise ValueError(f"Unexpected is_active value: {is_active}. Expected 'Active' or 'InActive'.")

    # Base message about the secret's status
    message = f"The provided secret '{service}' is currently {status}."
    
    # If a response exists, append it to the message
    if response:
        message += f" Here is the additional response data : \n{response_data}"

    return message
