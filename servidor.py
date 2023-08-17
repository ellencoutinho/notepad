import socket
from pathlib import Path
from utils import extract_route, read_file, build_response
from views import index
CUR_DIR = Path(__file__).parent

SERVER_HOST = 'localhost'
SERVER_PORT = 8080

# dizem para o programa se conectar à porta desejada e aguardar requisições
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()
    # accept() trava a execução do programa até que uma requisição seja recebida
    request = client_connection.recv(1024).decode() # dados enviados pelo cliente em no máximo 1024 bytes
    print('*'*100)
    print(request)

    route = extract_route(request)
    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request)
    else:
        response = build_response()
    client_connection.sendall(response)

    print('Um cliente se conectou!')

    client_connection.close()

server_socket.close()