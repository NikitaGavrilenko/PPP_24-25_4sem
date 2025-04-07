import socket
import json
import logging
import os

logging.basicConfig(filename='client.log', level=logging.INFO)
HOST = '127.0.0.1'
PORT = 9090

def get_file_list(sock):
    request = {"command": "list_files"}
    sock.sendall(json.dumps(request).encode())
    data = sock.recv(8192)
    files = json.loads(data.decode())
    print("Available audio files:")
    for f in files:
        print(f"- {f['filename']} ({f['duration']}s)")
    logging.info("Requested list of files")

def get_float_input(prompt):
    """Получение числа с проверкой"""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Время не может быть отрицательным")
                continue
            return value
        except ValueError:
            print("Пожалуйста, введите число")
def get_segment(sock):
    """Запрос отрезка аудио"""
    filename = input("Введите имя файла: ").strip()
    if not filename:
        print("Имя файла не может быть пустым")
        return

    print("Укажите временной интервал (в секундах)")
    while True:
        start = get_float_input("Начало: ")
        end = get_float_input("Конец: ")

        if start >= end:
            print("Конечное время должно быть больше начального")
        else:
            break

    request = {
        "command": "get_segment",
        "filename": filename,
        "start": start,
        "end": end
    }

    sock.sendall(json.dumps(request).encode())

    try:
        length = int(sock.recv(16).decode().strip())
        data = sock.recv(length)

        os.makedirs("downloads", exist_ok=True)
        out_file = f"downloads/{filename}_{start}-{end}.mp3"
        with open(out_file, 'wb') as f:
            f.write(data)
        print(f"Файл сохранен как {out_file}")

    except (ValueError, ConnectionError):
        print("Ошибка при получении данных. Возможно указано неверное имя файла.")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((HOST, PORT))
            print(f"Подключено к {HOST}:{PORT}")

            while True:
                cmd = input(
                    "\nКоманды:\n1. list - список файлов\n2. get - получить отрезок\n3. exit - выход\n> ").lower()

                if cmd == 'list':
                    sock.sendall(json.dumps({"command": "list_files"}).encode())
                    files = json.loads(sock.recv(4096).decode())
                    print("\nДоступные файлы:")
                    for f in files:
                        print(f"- {f['filename']} ({f['duration']:.1f} сек)")

                elif cmd == 'get':
                    get_segment(sock)

                elif cmd == 'exit':
                    break

                else:
                    print("Неизвестная команда")

        except ConnectionRefusedError:
            print("Сервер недоступен")
        finally:
            print("Соединение закрыто")

if __name__ == "__main__":
    main()