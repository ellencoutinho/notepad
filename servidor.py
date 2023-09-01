import socket
from pathlib import Path
from utils import extract_route, read_file, build_response, apaga_nota, load_template
from views import index, edit
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
    request = client_connection.recv(1024).decode() # dados enviados pelo cliente em no máximo 1024 bytes
    print('*'*100)
    print(request)

    route = extract_route(request)
    
    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request)
    elif request.split()[1].split('/')[1] == 'delete':
        response = apaga_nota(request.split()[1].split('/')[2])
    elif request.split()[1].split('/')[1] == 'edit':
        response = edit(request, id=request.split()[1].split('/')[2])

    else:
        response = build_response(code=404, body= load_template("erro404.html"))
    client_connection.sendall(response)

    print('Um cliente se conectou!')

    client_connection.close()

server_socket.close()