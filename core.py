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
        result = [i for i in self.data.split('\n') if 'local' in i]
        self.cert_dict = {}
        for i in result:
            stdin, stdout, stderr = self.client.exec_command(f'cert_mgr show -i {i[0]}')
            data_string = (str(stdout.read() + stderr.read(), encoding = 'utf-8'))

            lines = data_string.split('\n')[1:]
            self.result_dict = {}
            for line in lines:
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    self.result_dict[key.strip()] = value.strip()
            self.cert_dict[i[0]] = self.result_dict

        for key, value in self.cert_dict.items():

            valid_to_str = value.get('Valid to')
            if valid_to_str:
                expire_date = datetime.strptime(valid_to_str, "%a %b %d %H:%M:%S %Y")
                now = datetime.now().date()
                day_exp = (expire_date - now).days
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
            self.con.close()
            return f"Нет сертификатов с истекающим сроком действия более {days}"
