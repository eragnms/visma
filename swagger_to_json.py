"""A support function to save a Swagger definition to a file.


The function fetches a Swagger definition from a URL and saves it to a json
file. One can then run:
> swagger-marshmallow-codegen swagger.json > my_model.py, to generate a
marshmallow model from the Swagger definition.
"""

import requests


def save_swagger_definition(url, output_file):
    """Save a Swagger definition to a file."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        with open(output_file, 'w') as file:
            file.write(response.text)
        print(f"Swagger definition saved to {output_file}")
    except requests.RequestException as e:
        print(f"Error fetching Swagger definition from {url}: {e}")


# Example usage
swagger_url = "https://eaccountingapi.vismaonline.com:443/swagger/docs/v2"
output_file = "swagger.json"
save_swagger_definition(swagger_url, output_file)
