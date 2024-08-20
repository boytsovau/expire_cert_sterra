import paramiko  # type: ignore
from datetime import datetime


class ExpireCert:

    def __init__(self, hostname: str, username: str, password: str, port: int) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.data = ""

    def make_con(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.load_system_host_keys()
            self.client.connect(hostname=self.hostname, username=self.username, password=self.password, port=self.port)
            return self.client
            print(f"Succesful connected to {self.hostname}\n\n")
        except Exception as e:
            print(f"No connection to {self.hostname}: {e}\n\n")

    def send_command(self, command: str) -> str:
        if not self.client:
            return "No active connection."
        try:
            self.command = command
            stdin, stdout, stderr = self.client.exec_command(self.command)
            byte_data = stdout.read() + stderr.read()
            self.data = str(byte_data, encoding ='utf-8')
            return self.data
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def get_expire(self, days: int) -> str:
        if not self.data:
            return "No data to process."

        cert_dict = {}
        for line in self.data.splitlines():
            if 'local' in line:
                cert_id = line.split()[0]
                stdin, stdout, stderr = self.client.exec_command(f'cert_mgr show -i {cert_id}')
                data_string = (stdout.read() + stderr.read()).decode('utf-8')

                result_dict = {
                    key.strip(): value.strip()
                    for key, value in (line.split(': ', 1) for line in data_string.splitlines() if ': ' in line)
                }
                cert_dict[cert_id] = result_dict

        for key, value in self.cert_dict.items():

            valid_to_str = value.get('Valid to')
            if valid_to_str:
                expire_date = datetime.strptime(valid_to_str, "%a %b %d %H:%M:%S %Y")
                now = datetime.now().date()
                day_exp = (expire_date.date() - now).days
            if day_exp < days:
                cert_subject = value.get('Subject')
                cert_valid_date = value.get('Valid to')
                cert_issuer = value.get('Issuer')
                cert_serial = value.get('Serial number')
                self.client.close()
                return (f"Сертификат {cert_subject} просрочится через {day_exp} дней.\n\n"
                          f"Данные по сертификату:\n\n"
                          f"Subject: {cert_subject}\n"
                          f"Valid to: {cert_valid_date}\n"
                          f"Issuer: {cert_issuer}\n"
                          f"Serial: {cert_serial}")
            self.client.close()
            return f"Нет сертификатов со сроком действия менее {days} дней"
