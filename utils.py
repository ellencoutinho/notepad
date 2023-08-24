import json

def extract_route(requisicao):
    fatiamento = requisicao.split(" ")[1][1::]
    return fatiamento

def read_file(path):
    with open(path, mode='r+b') as file:
        return file.read()

def load_data(arquivo):
    path = f'data/{arquivo}'
    arquivo = read_file(path)
    conteudo = json.loads(arquivo)
    return conteudo

def load_template(template):
    path = f'templates/{template}'
    with open(path, mode='r', encoding="utf-8") as file:
        return str(file.read())
    
def load_note(anotacao):
    # recebe a nova anotação (dicionario) e a adiciona à lista do arquivo notes.json
    
    conteudo = load_data('notes.json')
    conteudo.append(anotacao)

    with open('data/notes.json', 'w') as file:
        json.dump(conteudo, file, indent=4)

def build_response(body='', code=200, reason='OK', headers=''):
    # 'HTTP/1.1 200 OK'
    if headers == '':
        response = 'HTTP/1.1' + ' ' + str(code) + ' ' + reason + '\n\n' + body
    else:
        response = 'HTTP/1.1' + ' ' + str(code) + ' ' + reason + '\n' + str(headers) + '\n\n' + body
    return response.encode()

