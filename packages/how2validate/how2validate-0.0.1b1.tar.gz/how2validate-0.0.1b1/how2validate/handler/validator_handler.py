# Create a mapping of service names to handler functions
from how2validate.validators.snyk.snyk_auth_key import validate_snyk_auth_key
from how2validate.validators.sonarcloud.sonarcloud_token import validate_sonarcloud_token
from how2validate.validators.npm.npm_access_token import validate_npm_access_token


service_handlers = {
    "snyk_auth_key": validate_snyk_auth_key,
    "sonarcloud_token": validate_sonarcloud_token,
    "npm_access_token": validate_npm_access_token
    # Add all your services here
}

def validator_handle_service(service, secret, response, report):
    # Get the handler function based on the service name
    handler = service_handlers.get(service)
    
    if handler:
        return handler(service, secret, response, report)
    else:
        return f"Error: No handler for service '{service}'"

