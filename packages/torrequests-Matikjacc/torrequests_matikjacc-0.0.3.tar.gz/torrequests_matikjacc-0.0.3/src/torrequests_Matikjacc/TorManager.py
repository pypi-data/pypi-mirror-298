import subprocess
import requests
import time
from stem import Signal
from stem.control import Controller

class TorManager:
    def __init__(self, tor_password, tor_port=9050, control_port=9051):
        self.tor_password = tor_password
        self.tor_port = tor_port
        self.control_port = control_port
        self.proxies = {
            'http': f'socks5h://127.0.0.1:{self.tor_port}',
            'https': f'socks5h://127.0.0.1:{self.tor_port}'
        }

    def is_tor_running(self):
        """Check if Tor is running by checking for its process or connectivity on Windows."""
        try:
            output = subprocess.check_output(['powershell', '-Command', 'Get-Process tor -ErrorAction SilentlyContinue'])
            return bool(output)
        except subprocess.CalledProcessError:
            return False

    def renew_tor_ip(self):
        """Request a new Tor circuit (new IP address)."""
        with Controller.from_port(port=self.control_port) as controller:
            controller.authenticate(password=self.tor_password)
            controller.signal(Signal.NEWNYM)
            print("New Tor IP requested")
            time.sleep(10)  # Wait for Tor to establish a new circuit

    def make_tor_request(self, url, method='GET', headers=None, params=None, data=None, json=None):
        """Make a request through Tor with support for different methods (GET, POST, PUT, DELETE)."""
        try:
            # Select the appropriate request method
            method = method.upper()
            if method == 'GET':
                response = requests.get(url, proxies=self.proxies, headers=headers, params=params)
            elif method == 'POST':
                response = requests.post(url, proxies=self.proxies, headers=headers, params=params, data=data, json=json)
            elif method == 'PUT':
                response = requests.put(url, proxies=self.proxies, headers=headers, params=params, data=data, json=json)
            elif method == 'DELETE':
                response = requests.delete(url, proxies=self.proxies, headers=headers, params=params)
            else:
                print(f"Unsupported HTTP method: {method}")
                return False
            
            response_text = response.text.strip()
            response_code = response.status_code

            return (response_text, response_code)
        except requests.RequestException as e:
            print(f"Failed to make Tor request: {e}")
            return False
