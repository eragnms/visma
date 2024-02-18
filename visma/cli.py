import click
import webbrowser
import requests
import datetime
import json
from os import environ
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from urllib.parse import urlparse, parse_qs

@click.group()
def cli():
    pass

@cli.command()
@click.option('--client', default='', help='Client ID')
@click.option('--redirect', default='', help='Redirect URI')
@click.option('--browser', default='firefox', help='Specify browser')
@click.option('--production', is_flag=True, )
def request_access(client, redirect, browser, production):
    click.echo('Opening webpage')

    if client == '':
        client = environ.get('VISMA_API_CLIENT_ID')
    if redirect == '':
        redirect = environ.get('VISMA_API_REDIRECT_URI')

    __browser = webbrowser.get(browser)

    if production:
        __browser.open((f'https://identity.vismaonline.com/connect/authorize'
                        f'?client_id='
                        f'{client}&redirect_uri=https://identity.vismaonline'
                        f'.com/redirect_receiver&scope=ea:api%20offline_access'
                        f'%20ea:sales%20ea:accounting%20ea:purchase&state=FromPythonCLI&response_type=code'
                        f'&prompt=login'), new=1)
    else:
        sandbox_acc = (
            f'https://identity-sandbox.test.vismaonline.com'
            f'/connect/authorize'
            f'?client_id={client}&'
            f'redirect_uri={redirect}'
            f'&scope=ea:api%20offline_access'
            f'%20ea:sales%20ea:accounting%20ea:purchase&state=FromPythonCLI&response_type=code'
            f'&prompt=login'
        )
        # In case the below fetching the code automatically does not work uncomment the below line
        # __browser.open(sandbox_acc, new=1)

        # Open Firefox browser
        driver = webdriver.Firefox()
        # Open the initial page
        driver.get(sandbox_acc)
        # Wait for page to load
        time.sleep(2)  # Adjust this wait time as needed
        # After the page loads, you can manually enter your credentials in the browser
        # You can interact with the browser as you would normally do
        # Wait for the user to manually enter credentials and perform login
        input("Press Enter after logging in...")
        # After login, the server will redirect to a new page
        # Get the current URL
        new_page_url = driver.current_url
        print("URL of the new page:", new_page_url)
        # Close the browser
        driver.quit()
        url = new_page_url
        # Parse the URL
        parsed_url = urlparse(url)
        # Extract query parameters
        query_params = parse_qs(parsed_url.query)
        # Access the value of the "code" parameter
        code = query_params.get('code')
        print("Code:", code[0] if code else "Not found")
        get_token_non_cli(code[0], client, '', redirect, '', production)


@cli.command()
@click.option('--code', prompt=True, help='Client ID')
@click.option('--client', default='', help='Client ID')
@click.option('--secret', default='', help='Client ID')
@click.option('--redirect', default='', help='Redirect URI')
@click.option('--tokenfile', default='', help='Filename to save token to')
@click.option('--production', is_flag=True, )
def get_token(code, client, secret, redirect, tokenfile, production):
    get_token_non_cli(code, client, secret, redirect, tokenfile, production)


def get_token_non_cli(code, client, secret, redirect, tokenfile, production):
    if client == '':
        client = environ.get('VISMA_API_CLIENT_ID')
    if redirect == '':
        redirect = environ.get('VISMA_API_REDIRECT_URI')
    if secret == '':
        secret = environ.get('VISMA_API_CLIENT_SECRET')
    if tokenfile == '':
        tokenfile = environ.get('VISMA_API_TOKEN_PATH')

    TEST_URL = 'https://identity-sandbox.test.vismaonline.com/connect/token'
    PROD_URL = 'https://identity.vismaonline.com/connect/token'
    credentials = (client, secret)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    data = f'grant_type=authorization_code&code={code}&redirect_uri={redirect}'

    if production:
        response = requests.post(PROD_URL, data,  auth=credentials, headers=headers)
    else:
        response = requests.post(TEST_URL, data,  auth=credentials, headers=headers)

    auth_info = response.json()
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    # removes a minute so we dont end up not beeing authenticated because of
    # time difference between client and server.
    expires = now + datetime.timedelta(
        seconds=(auth_info.get('expires_in', 60)-60))
    auth_info['expires'] = expires.isoformat()

    print(json.dumps(auth_info))

    with open(tokenfile, 'w') as json_file:
        json.dump(auth_info, json_file, indent=4)
