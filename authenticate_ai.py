import os
import configparser
import openai

def create_session(OPENAI_API_KEY, OPENAI_ENDPOINT):
    """
    Create a session with the OpenAI API by reading credentials from a configuration file and setting up SSL certificates.

    Returns:
        tuple: A tuple containing the OpenAI client object and the username.
    
    Raises:
        ValueError: If the username or key is missing in the configuration file.
        FileNotFoundError: If the configuration file is not found.
        Exception: For any other errors that occur during execution.
    """
    try:
        # Set the path for the PEM file used for SSL certificate verification
        pem_path = "/usr/local/etc/openssl@3/certs/../cert.pem"
        os.environ['REQUESTS_CA_BUNDLE'] = pem_path
        os.environ['SSL_CERT_FILE'] = pem_path

        
        # Create an instance of the OpenAI client
        client = openai.OpenAI(
            base_url=OPENAI_ENDPOINT,
            api_key=OPENAI_API_KEY
        )

        # Return the client object and the username
        return client
    
    except FileNotFoundError as fnf_error:
        print(f"Error: {fnf_error}")
        raise
    except configparser.Error as config_error:
        print(f"Error parsing configuration file: {config_error}")
        raise
    except openai.error.OpenAIError as openai_error:
        print(f"Error creating OpenAI client: {openai_error}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

