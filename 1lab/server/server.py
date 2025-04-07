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
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)
        logging.warning(f"Created missing audio directory: {AUDIO_DIR}")
        return metadata

    for file in os.listdir(AUDIO_DIR):
        if file.endswith(('.mp3', '.wav')):
            path = os.path.join(AUDIO_DIR, file)
            try:
                audio = AudioSegment.from_file(path)
                metadata.append({
                    "filename": file,
                    "duration": len(audio) / 1000,  # в секундах
                    "format": file.split('.')[-1]
                })
            except Exception as e:
                logging.error(f"Error processing {file}: {e}")
                continue

    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f)
    return metadata

def handle_client(conn, addr):
    logging.info(f"Client connected: {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data or data.strip() == "":
                logging.warning(f"Empty request from {addr}")
                conn.sendall(json.dumps({"error": "Empty request"}).encode())
                break

            try:
                request = json.loads(data)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON from {addr}: {data}")
                conn.sendall(json.dumps({"error": "Invalid JSON format"}).encode())
                break

            command = request.get("command")
            if not command:
                logging.error(f"Missing command from {addr}")
                conn.sendall(json.dumps({"error": "Missing command"}).encode())
                break

            if command == "list_files":
                try:
                    with open(METADATA_FILE) as f:
                        metadata = json.load(f)
                    response = json.dumps(metadata).encode()
                    conn.sendall(response)
                except Exception as e:
                    logging.error(f"Error listing files: {e}")
                    conn.sendall(json.dumps({"error": str(e)}).encode())

            elif command == "get_segment":
                try:
                    if not all(k in request for k in ["filename", "start", "end"]):
                        raise ValueError("Missing required fields (filename, start, end)")

                    filename = request["filename"]
                    if not filename or not isinstance(filename, str):
                        raise ValueError("Invalid filename")

                    try:
                        start = float(request["start"]) * 1000
                        end = float(request["end"]) * 1000
                    except (ValueError, TypeError):
                        raise ValueError("Start and end must be numbers")

                    full_path = os.path.join(AUDIO_DIR, filename)
                    if not os.path.exists(full_path):
                        raise FileNotFoundError("File not found")

                    audio = AudioSegment.from_file(full_path)
                    if start < 0 or end > len(audio) or start >= end:
                        raise ValueError("Invalid time range")

                    segment = audio[start:end]

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
                        segment.export(tmpfile.name, format="mp3")
                        tmpfile.seek(0)
                        with open(tmpfile.name, 'rb') as f:
                            segment_data = f.read()

                    conn.sendall(str(len(segment_data)).encode().ljust(16))
                    conn.sendall(segment_data)
                    logging.info(f"Sent segment {filename} [{start}-{end}] to {addr}")

                except Exception as e:
                    logging.error(f"Error processing segment: {e}")
                    conn.sendall(json.dumps({"error": str(e)}).encode())

            else:
                logging.warning(f"Unknown command from {addr}: {command}")
                conn.sendall(json.dumps({"error": "Unknown command"}).encode())

    except Exception as e:
        logging.error(f"Connection error with {addr}: {e}")
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
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
            except Exception as e:
                logging.error(f"Server error: {e}")

if __name__ == "__main__":
    main()