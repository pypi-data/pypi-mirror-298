import argparse
import json
import logging
import os
import subprocess
import sys

from tabulate import tabulate

from how2validate.utility.config_utility import get_package_name
from how2validate.utility.log_utility import setup_logging

# Call the logging setup function
setup_logging()

# Get the directory of the current file
current_dir = os.path.dirname(__file__)

# Path to the TokenManager JSON file
file_path = os.path.join(current_dir, '..', '..', 'tokenManager.json')

def get_secretprovider(file_path = file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    enabled_secrets_services = []
    
    for provider, tokens in data.items():
        for token_info in tokens:
            if token_info['is_enabled']:
                enabled_secrets_services.append(f"{provider}")
    
    return enabled_secrets_services

def get_secretservices(file_path = file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    enabled_secrets_services = []
    
    for provider, tokens in data.items():
        for token_info in tokens:
            if token_info['is_enabled']:
                enabled_secrets_services.append(f"{token_info['display_name']}")
    
    return enabled_secrets_services

def get_secretscope(file_path = file_path):
    """
    Reads a JSON file containing provider tokens and logs a table of enabled services.

    Args:
        file_path (str): The path to the JSON file containing provider tokens. 
                         Defaults to the global variable `file_path`.

    Raises:
        FileNotFoundError: If the specified file cannot be found or read.
    
    Returns:
        None: This function logs a formatted table of enabled provider services.
              If no enabled services are found, it logs a relevant message.
    """
    # Open and load the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    scoped_services = []

    # Iterate over each provider and its tokens
    for provider, tokens in data.items():
        for token_info in tokens:
            # Check if the token is enabled
            if token_info['is_enabled']:
                # Add the provider and service (token display name) to the scoped services list
                scoped_services.append([provider, token_info['display_name']])

    # Log the result as a table
    if scoped_services:
        # Log the table using the tabulate function with fancy formatting
        logging.info(tabulate(scoped_services, headers=['Provider', 'Service'], tablefmt='fancy_outline'))
    else:
        # Log a message if no enabled services are found
        logging.info("No enabled services found.")

def format_serviceprovider(file_path = file_path):
    """Format service choices as a bullet-point list."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    enabled_secrets_services = []
    
    for provider, tokens in data.items():
        for token_info in tokens:
            if token_info['is_enabled']:
                enabled_secrets_services.append(f"{provider}")

    return "\n".join([f"  - {service}" for service in enabled_secrets_services])

def format_services(file_path = file_path):
    """Format service choices as a bullet-point list."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    enabled_secrets_services = []
    
    for provider, tokens in data.items():
        for token_info in tokens:
            if token_info['is_enabled']:
                enabled_secrets_services.append(f"{provider} - {token_info['display_name']}")

    return "\n".join([f"  - {service}" for service in enabled_secrets_services])

def format_string(input_string):
    """
    Converts a string to lowercase and replaces spaces with underscores.

    Args:
        input_string (str): The input string to format.

    Returns:
        str: The formatted string with lowercase and underscores.
    """
    if not isinstance(input_string, str):
        raise ValueError("Input must be a string")
    
    return input_string.lower().replace(' ', '_')

def validate_choice(value, valid_choices):
    """
    Validates if the provided value is among the valid choices after formatting.

    Args:
        value (str): The input value to validate.
        valid_choices (list): The list of valid choices.

    Raises:
        argparse.ArgumentTypeError: If the value is not in valid_choices.

    Returns:
        str: The formatted and validated value.
    """
    formatted_value = format_string(value)
    formatted_choices = [format_string(choice) for choice in valid_choices]  # Format valid choices

    if formatted_value not in formatted_choices:
        raise argparse.ArgumentTypeError(
            f"Invalid choice: '{value}'. Choose from {', '.join(valid_choices)}."
        )
    
    return formatted_value

def redact_secret(secret):
    """
    Redacts a secret by keeping the first 5 characters and replacing the rest with asterisks.

    Args:
        secret (str): The secret string to redact.

    Returns:
        str: The redacted secret.
    """
    if not isinstance(secret, str):
        raise ValueError("Input must be a string")
    
    if len(secret) <= 5:
        return secret  # Return the secret as is if it's 5 characters or less

    return secret[:5] + '*' * (len(secret) - 5)

def update_tool():
    """Update the tool to the latest version."""
    logging.info("Updating the tool...")
    # Use 'pip3' for Python 3.x and 'pip' for Python 2.x or if Python 3.x is the default interpreter
    pip_command = "pip3" if sys.version_info.major == 3 else "pip"
    try:
        subprocess.run([pip_command, "install", "--upgrade",
                       f"{get_package_name()}"], check=True)
        print("Tool updated to the latest version.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update the tool: {e}")