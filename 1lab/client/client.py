import socket
import json
import logging

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

def get_segment(sock):
    filename = input("Enter filename: ")
    start = input("Start time (sec): ")
    end = input("End time (sec): ")

    request = {
        "command": "get_segment",
        "filename": filename,
        "start": start,
        "end": end
    }
    sock.sendall(json.dumps(request).encode())

    length = int(sock.recv(16).decode().strip())
    data = b''
    while len(data) < length:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet

    out_path = f"downloads/{filename.split('.')[0]}_{start}_{end}.mp3"
    with open(out_path, 'wb') as f:
        f.write(data)
    print(f"Segment saved to {out_path}")
    logging.info(f"Downloaded segment of {filename}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print("Connected to server.")

        while True:
            cmd = input("Enter command (list/get/exit): ").strip().lower()
            if cmd == 'list':
                get_file_list(sock)
            elif cmd == 'get':
                get_segment(sock)
            elif cmd == 'exit':
                break
            else:
                print("Unknown command")

if __name__ == "__main__":
    main()