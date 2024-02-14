import requests

# Set your Ecobee API key
API_KEY = 'YOUR_API_KEY'

# Authentication endpoint URL
AUTH_URL = 'https://api.ecobee.com/token'

# Thermostat data endpoint URL
THERMOSTAT_URL = 'https://api.ecobee.com/1/thermostat'

def authenticate():
    # Authentication payload
    auth_payload = {
        'grant_type': 'ecobeePin',
        'client_id': API_KEY
    }

    # Make request to get pin and authorization code
    response = requests.post(AUTH_URL, json=auth_payload)
    auth_data = response.json()

    # Display pin and prompt user to authorize
    print("Pin:", auth_data['ecobeePin'])
    print("Please authorize the application using this pin.")
    input("Press Enter when authorized...")

    # Authorization payload
    auth_payload = {
        'grant_type': 'ecobeePin',
        'code': auth_data['code'],
        'client_id': API_KEY
    }

    # Request access token
    response = requests.post(AUTH_URL, json=auth_payload)
    access_token = response.json()['access_token']

    return access_token

def get_thermostat_info(access_token):
    # Request thermostat information
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(THERMOSTAT_URL, headers=headers)
    thermostat_data = response.json()

    return thermostat_data

def main():
    # Authenticate and get access token
    access_token = authenticate()

    # Get thermostat information
    thermostat_info = get_thermostat_info(access_token)
    print("Thermostat Information:")
    print(thermostat_info)

if __name__ == "__main__":
    main()
