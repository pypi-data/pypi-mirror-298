import requests
import platform
import subprocess

class AuthVault:
    def __init__(self):
        self.is_valid_key = False

    def get_hwid(self):
        cpu_info = platform.processor()

        try:
            result = subprocess.check_output('wmic diskdrive get serialnumber', shell=True)
            disk_serial = result.decode().split('\n')[1].strip()
        except Exception as e:
            disk_serial = 'unknown'

        hwid = cpu_info + disk_serial
        return hwid

    def authvault(self, license_key, application_id, secret):
        hwid = self.get_hwid()

        url = f"http://localhost/shittyahh.php?license_key={license_key}&application_id={application_id}&secret={secret}&hwid={hwid}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                response_data = response.json()
                status = response_data.get("status")

                if status == "valid":
                    self.is_valid_key = True
                elif status == "invalid":
                    self.is_valid_key = False
            else:
                print(f"HTTP Error: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def get_auth_status(self):
        return self.is_valid_key
