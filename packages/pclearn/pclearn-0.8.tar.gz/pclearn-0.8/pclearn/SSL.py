import socket
import ssl
def fetch_https_content(hostname):
    context = ssl.create_default_context() 
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            print(ssock.version())
            request = f"GET / HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n"
            ssock.sendall(request.encode())
            response = ssock.recv(4096)
            print(response.decode())
fetch_https_content("www.python.org")
