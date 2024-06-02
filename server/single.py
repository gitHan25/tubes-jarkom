import socket
import os

def handle_request(request):
    """Fungsi untuk menangani request HTTP dan membentuk response."""
    # Memparsing request HTTP
    lines = request.split("\r\n")
    request_line = lines[0]
    print(f"Request Line: {request_line}")

    # Mendapatkan method, path, dan HTTP version dari request line
    method, path, version = request_line.split()
    file_path = path.strip("/")

    # Menentukan file default jika path kosong
    if file_path == "":
        file_path = "index.html"

    # Membentuk response berdasarkan apakah file ada atau tidak
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            content = file.read()
            response_line = "HTTP/1.1 200 OK\r\n"
            headers = "Content-Type: text/html; charset=UTF-8\r\n"
            headers += f"Content-Length: {len(content)}\r\n"
            headers += "\r\n"
            response = response_line.encode() + headers.encode() + content
    else:
        response_line = "HTTP/1.1 404 Not Found\r\n"
        headers = "Content-Type: text/html; charset=UTF-8\r\n"
        headers += "\r\n"
        body = "<html><body><h1>404 Not Found</h1></body></html>"
        response = response_line.encode() + headers.encode() + body.encode()

    return response

def server_start():
    """Fungsi untuk memulai server web."""
    SERVER_HOST = '192.168.1.17'  # Alamat IP server
    SERVER_PORT = 3000            # Port server
        # Ukuran buffer untuk menerima data

    # Membuat server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)

    print(f"\nServer is running on http://{SERVER_HOST}:{SERVER_PORT}\n\n")

    while True:
        # Menerima koneksi dari klien
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Menerima data request dari klien
        request_data = client_socket.recv(1024).decode()
        print(f"Request Data:\n{request_data}")

        # Membentuk response HTTP
        response = handle_request(request_data)
        

        # Mengirim response ke klien
        client_socket.sendall(response)
        client_socket.close()

if __name__ == "__main__":
    server_start()
