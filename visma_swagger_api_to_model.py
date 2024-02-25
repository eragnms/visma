"""A support function to create the model.py file.

Takes the URL of the Visma eAccounting API Swagger definition and saves it
to a marchmallow model file that can be used by the package visma.
"""

import subprocess
import requests
import yaml
import os
import logging


def setup_logging():
    """Set up logging to the console."""
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


def fetch_swagger_definition(url):
    """Fetch a Swagger definition from a URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching Swagger definition from {url}: {e}")
        return None


def convert_to_yaml(swagger_definition, output_file):
    """Convert a Swagger definition to YAML and saves it to a file."""
    try:
        with open(output_file, "w") as file:
            yaml.dump(swagger_definition, file, default_flow_style=False)
        print(f"Swagger definition saved to {output_file}")
    except Exception as e:
        print(f"Error writing Swagger definition to {output_file}: {e}")


def generate_model(swagger_yaml_file, output_file):
    """Generate a model file from a Swagger definition."""
    try:
        with open(output_file, 'w') as f:
            subprocess.run(['swagger-marshmallow-codegen', swagger_yaml_file], stdout=f, check=True)
        print(f"Model file generated: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error generating model: {e}")


def delete_file(file_path):
    """Delete a file."""
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully")
    except OSError as e:
        print(f"Error deleting file '{file_path}': {e}")


swagger_url = "https://eaccountingapi.vismaonline.com:443/swagger/docs/v2"
yaml_file = "swagger.yaml"  # This is just a temporary file
model_file = "my_model.py"

setup_logging()
swagger_definition = fetch_swagger_definition(swagger_url)
if swagger_definition:
    convert_to_yaml(swagger_definition, yaml_file)
    generate_model(yaml_file, model_file)
    delete_file(yaml_file)
else:
    print("Failed to fetch Swagger definition")
