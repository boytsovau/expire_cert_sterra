from core import ExpireCert
import argparse


def main():
    parser = argparse.ArgumentParser(description="Проверка на срок действия сертификата.")
    parser.add_argument('--hostname', nargs='+', required=True, help="список ip")
    parser.add_argument('--username', required=True, help="Пользователь для подключения")
    parser.add_argument('--password', required=True, help="Пароль для подключения.")
    parser.add_argument('--port', type=int, default=22, help="Пароль для подключения.")
    parser.add_argument('--command', type=str, required=True, help="команда для выполнения.")
    parser.add_argument('--command', type=int, default=30, help="Дней до конца сертификата. По умолчанию 30")

    args = parser.parse_args()

    for host in args.hostname:
        con = ExpireCert(host, args.username, args.password, args.port)
        con.make_con()
        con.send_command(args.command)
        print(f"{host}\n{con.get_expire(args.days)}")

if __name__ == "__main__":
    main()
