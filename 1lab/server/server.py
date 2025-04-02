import os
import json
import socket
import threading
import logging
import tempfile
from pydub import AudioSegment

AUDIO_DIR = "audiofiles"
METADATA_FILE = "audio_metadata.json"
HOST = '0.0.0.0'
PORT = 9090

logging.basicConfig(filename='server.log', level=logging.INFO)

def extract_metadata():
    metadata = []
    for file in os.listdir(AUDIO_DIR):
        if file.endswith(('.mp3', '.wav')):
            path = os.path.join(AUDIO_DIR, file)
            audio = AudioSegment.from_file(path)
            metadata.append({
                "filename": file,
                "duration": len(audio) / 1000,  # в секундах
                "format": file.split('.')[-1]
            })
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)
    return metadata

def handle_client(conn, addr):
    logging.info(f"Client connected: {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            request = json.loads(data)
            command = request.get("command")

            if command == "list_files":
                with open(METADATA_FILE) as f:
                    metadata = json.load(f)
                response = json.dumps(metadata).encode()
                conn.sendall(response)

            elif command == "get_segment":
                filename = request["filename"]
                start = float(request["start"]) * 1000
                end = float(request["end"]) * 1000
                full_path = os.path.join(AUDIO_DIR, filename)

                audio = AudioSegment.from_file(full_path)
                segment = audio[start:end]

                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                    segment.export(tmpfile.name, format="mp3")
                    tmpfile.seek(0)
                    with open(tmpfile.name, 'rb') as f:
                        segment_data = f.read()

                # Отправка длины
                conn.sendall(str(len(segment_data)).encode().ljust(16))
                # Отправка данных
                conn.sendall(segment_data)
                logging.info(f"Sent segment {filename} [{start}-{end}] to {addr}")

    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        conn.close()
        logging.info(f"Client disconnected: {addr}")

def main():
    extract_metadata()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logging.info(f"Server started on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == "__main__":
    main()