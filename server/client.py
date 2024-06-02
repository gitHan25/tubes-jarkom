import socket
import sys

def http_client(server_host, server_port, filename):
    # Membuat socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Menghubungkan ke server
    client_socket.connect((server_host, int(server_port)))
    
    # Membentuk request GET
    request_line = f"GET /{filename} HTTP/1.1\r\n"
    headers = f"Host: {server_host}:{server_port}\r\n"
    headers += "Connection: close\r\n"
    headers += "\r\n"
    request = request_line + headers
    
    # Mengirim request ke server
    client_socket.sendall(request.encode())
    
    # Menerima respons dari server
    response = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        response += data
    
    # Menutup koneksi
    client_socket.close()
    
    # Menampilkan respons
    print(response.decode())

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: client.py server_host server_port filename")
        sys.exit(1)
    
    server_host = sys.argv[1]
    server_port = sys.argv[2]
    filename = sys.argv[3]
    
    http_client(server_host, server_port, filename)
