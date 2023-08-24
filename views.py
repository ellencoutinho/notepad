from utils import load_data, load_template, load_note, build_response
from urllib.parse import unquote_plus

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]

        params = {}
        # Preencha o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        # Dica: use o método split da string e a função unquote_plus (ela deixa o texto legível)
        for chave_valor in corpo.split('&'):
            conteudo_valor = chave_valor.split('=')
            chave = unquote_plus(conteudo_valor[0])
            valor = unquote_plus(conteudo_valor[1])
            params[chave] = valor
        load_note(params)
        return(build_response(code=303, reason='See Other', headers='Location: /'))

    # Cria uma lista de <li>'s para cada anotação
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados['titulo'], details=dados['detalhes'])
        for dados in load_data('notes.json')
    ]
    notes = '\n'.join(notes_li)
    response = build_response(body=load_template('index.html').format(notes=notes))

    return response