import os
from dotenv import load_dotenv

def load_env_variables():
    """
    Utility for loading env variables from multiple places.

    If loaded from individual file, env is at ../../.env
    If loaded in container, env is at ../.env
    If loaded as container with ENV set they are in normal environment
    """
    # Load local .env for prod
    if os.path.exists(".env"):
        load_dotenv()

    # Load in the middle I guess 
    elif os.path.exists("../.env"): 
        load_dotenv("../.env")
        
    # Load root .env if dev
    elif os.path.exists("../../.env"):
        load_dotenv('../../.env')

    # Exit if neither
    else:
        raise FileNotFoundError("Neither local .env nor fallback .env file found")

def get_env_variable(variable_name):
    """
    Loads the specified environment variable.

    Parameters:
        variable_name (str): The name of the environment variable to retrieve.

    Returns:
        str: The value of the specified environment variable.

    Raises:
        RuntimeError: If the specified environment variable is not found.
    """
    # Loads from .env file
    load_env_variables()

    # First, check if the variable exists in environment variables
    env_value = os.getenv(variable_name)

    # Then, check if the variable exists in the .env file
    if env_value is None:
        env_value = os.getenv(variable_name.upper())  # Try upper case

    if env_value is None:
        raise RuntimeError(f"Environment variable '{variable_name}' not found")

    return env_value
