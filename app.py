from flask import Flask, jsonify, request

app = Flask(__name__)

# Dados em memória (simulando um banco)
tarefas = [
    {"id": 1, "titulo": "Estudar Python", "concluida": False},
    {"id": 2, "titulo": "Fazer testes", "concluida": True}
]
proximo_id = 3

@app.route('/')
def home():
    """Endpoint raiz"""
    return jsonify({"mensagem": "API funcionando!", "status": "online"})

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    """Lista todas as tarefas"""
    return jsonify(tarefas)

@app.route('/tarefas/<int:id>', methods=['GET'])
def buscar_tarefa(id):
    """Busca uma tarefa específica"""
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa:
        return jsonify(tarefa)
    return jsonify({"erro": "Tarefa não encontrada"}), 404

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    """Cria uma nova tarefa"""
    global proximo_id
    
    dados = request.get_json()
    
    if not dados or 'titulo' not in dados:
        return jsonify({"erro": "Título é obrigatório"}), 400
    
    nova_tarefa = {
        "id": proximo_id,
        "titulo": dados['titulo'],
        "concluida": dados.get('concluida', False)
    }
    
    tarefas.append(nova_tarefa)
    proximo_id += 1
    
    return jsonify(nova_tarefa), 201

@app.route('/tarefas/<int:id>', methods=['PUT'])
def atualizar_tarefa(id):
    """Atualiza uma tarefa existente"""
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    
    dados = request.get_json()
    
    if 'titulo' in dados:
        tarefa['titulo'] = dados['titulo']
    if 'concluida' in dados:
        tarefa['concluida'] = dados['concluida']
    
    return jsonify(tarefa)

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def deletar_tarefa(id):
    """Deleta uma tarefa"""
    global tarefas
    
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    
    tarefas = [t for t in tarefas if t["id"] != id]
    return jsonify({"mensagem": "Tarefa deletada com sucesso"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)