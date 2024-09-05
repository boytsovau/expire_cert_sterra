from core import ExpireCert
import argparse


def main():
    parser = argparse.ArgumentParser(description="Проверка на срок действия сертификата.")
    parser.add_argument('--hostname', nargs='+', required=True, help="список ip")
    parser.add_argument('--username', required=True, help="Пользователь для подключения")
    parser.add_argument('--password', required=True, help="Пароль для подключения.")
    parser.add_argument('--port', type=int, default=22, help="Порт для подключения. По умолчанию 22")
    parser.add_argument('--command', type=str, default='cert_mgr show', help="команда для выполнения. По умолчанию cert_mgr show")
    parser.add_argument('--days', type=int, default=30, help="Дней до конца сертификата. По умолчанию 30")

    args = parser.parse_args()

    for host in args.hostname:
        try:
            con = ExpireCert(host, args.username, args.password, args.port)
            if not con.make_con():
                continue
            con.send_command(args.command)
            exp = con.get_expire(args.days)
            print(f"\nHOST: {host}\n\n{exp}")
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()
