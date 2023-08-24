from utils import load_data, load_template, load_note, build_response
from urllib.parse import unquote_plus
from database import Note

def index(request):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        lista = corpo.split('&')
        titulo = lista[0].split('=')[1]
        conteudo = lista[1].split('=')[1]
        load_note(Note(title=titulo, content=conteudo))

        return(build_response(code=303, reason='See Other', headers='Location: /'))

    # Cria uma lista de <li>'s para cada anotação
    note_template = load_template('components/note.html')
    notes_li = [
        note_template.format(title=dados.title, details=dados.content)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)
    response = build_response(body=load_template('index.html').format(notes=notes))

    return response