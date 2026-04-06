import os
from supabase import create_client
from flask import Flask, jsonify, request
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega as variáveis de ambiente
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Verifica se as variáveis foram carregadas corretamente
if not url or not key:
    raise ValueError("Erro: SUPABASE_URL e SUPABASE_KEY devem estar configuradas no arquivo .env")

supabase = create_client(url, key)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensagem": "API funcionando!", "status": "online"})


# GET todas tarefas
@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    response = supabase.table("tarefas").select("*").execute()
    return jsonify(response.data)


# GET por ID
@app.route('/tarefas/<int:id>', methods=['GET'])
def buscar_tarefa(id):
    response = supabase.table("tarefas").select("*").eq("id", id).execute()
    
    if response.data:
        return jsonify(response.data[0])
    return jsonify({"erro": "Tarefa não encontrada"}), 404


# POST
@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()

    if not dados or 'titulo' not in dados:
        return jsonify({"erro": "Título é obrigatório"}), 400

    response = supabase.table("tarefas").insert({
        "titulo": dados['titulo'],
        "concluida": dados.get('concluida', False)
    }).execute()

    return jsonify(response.data[0]), 201


# PUT
@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    dados = request.get_json()

    response = supabase.table("tarefas").update(dados).eq("id", id).execute()

    if response.data:
        return jsonify(response.data[0])
    return jsonify({"erro": "Tarefa não encontrada"}), 404


# DELETE
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    response = supabase.table("tarefas").delete().eq("id", id).execute()

    if response.data:
        return jsonify({"mensagem": "Tarefa deletada"})
    return jsonify({"erro": "Tarefa não encontrada"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
