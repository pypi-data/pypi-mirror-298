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

    def start_tor(self):
        """Start the Tor service using PowerShell if it's not already running."""
        if not self.is_tor_running():
            print("Starting Tor...")
            try:
                subprocess.Popen(['powershell', '-Command', 'Start-Tor'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(10)  # Wait for Tor to start
            except Exception as e:
                print(f"Failed to start Tor: {e}")

    def stop_tor(self):
        """Stop the Tor service by killing the process using PowerShell."""
        if self.is_tor_running():
            try:
                print("Stopping Tor...")
                # Use PowerShell to stop the tor.exe process
                subprocess.run(['powershell', '-Command', 'Stop-Process -Name tor -Force'], check=True)
                print("Tor has been stopped.")
            except subprocess.CalledProcessError as e:
                print(f"Failed to stop Tor: {e}")

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
                return
            
            print(f"Tor request successful: {response.status_code} - {response.text.strip()}")
        except requests.RequestException as e:
            print(f"Failed to make Tor request: {e}")


    def is_vpn_active(self):
        """Dummy VPN check (can be customized)."""
        # Add your VPN check logic here
        return True

    def execute(self, url, change_ip_every=5):
        """Main execution flow: check VPN, Tor, and make requests, changing IP periodically."""

        # Make requests through Tor, changing IP every few requests
        for i in range(change_ip_every * 2):
            self.make_tor_request(url)
            if (i + 1) % change_ip_every == 0:
                self.renew_tor_ip()

        # Optionally, stop Tor after the operations are done
        self.stop_tor()
