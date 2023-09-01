from utils import load_data, load_template, load_note, build_response, id_correspondente, edit_note
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
        titulo = unquote_plus(lista[0].split('=')[1])
        conteudo = unquote_plus(lista[1].split('=')[1])
        load_note(Note(title=titulo, content=conteudo))
        return(build_response(code=303, reason='See Other', headers='Location: /')) # recarrega pagina
    
    # Cria uma lista de <li>'s para cada anotação
    note_template = load_template('components/note.html')

    notes_li = [
        note_template.format(title=dados.title, details=dados.content, id=dados.id)
        for dados in load_data()
    ]
    notes = '\n'.join(notes_li)
    response = build_response(body=load_template('index.html').format(notes=notes))

    return response

def edit(request, id):
    # A string de request sempre começa com o tipo da requisição (ex: GET, POST)
    if request.startswith('POST'):
        # Update valor da base de dados com base no id


        request = request.replace('\r', '')  # Remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        partes = request.split('\n\n')
        corpo = partes[1]
        lista = corpo.split('&')
        titulo = unquote_plus(lista[0].split('=')[1])
        conteudo = unquote_plus(lista[1].split('=')[1])
        edit_note(Note(id=id, title=titulo, content=conteudo))
        return(build_response(code=303, reason='See Other', headers='Location: /')) # recarrega pagina
    
    title, content = id_correspondente(id)
    response = build_response(body=load_template('edit.html').format(title=title, content=content))
    

    return response