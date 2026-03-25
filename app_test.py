import pytest
from app import app

@pytest.fixture
def client():
    """Fixture para criar um cliente de teste"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Testa o endpoint raiz"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'online'
    assert 'mensagem' in data

def test_listar_tarefas(client):
    """Testa listagem de tarefas"""
    response = client.get('/tarefas')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_buscar_tarefa_existente(client):
    """Testa busca de tarefa que existe"""
    response = client.get('/tarefas/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == 1
    assert data['titulo'] == 'Estudar Python'

def test_buscar_tarefa_inexistente(client):
    """Testa busca de tarefa que não existe"""
    response = client.get('/tarefas/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'erro' in data

def test_criar_tarefa_sucesso(client):
    """Testa criação de tarefa com dados válidos"""
    response = client.post('/tarefas', 
                          json={'titulo': 'Nova tarefa'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == 'Nova tarefa'
    assert data['concluida'] == False
    assert 'id' in data

def test_criar_tarefa_sem_titulo(client):
    """Testa criação de tarefa sem título (deve falhar)"""
    response = client.post('/tarefas', 
                          json={'concluida': True})
    assert response.status_code == 400
    data = response.get_json()
    assert 'erro' in data

def test_atualizar_tarefa(client):
    """Testa atualização de tarefa"""
    response = client.put('/tarefas/1',
                         json={'titulo': 'Título atualizado', 
                               'concluida': True})
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Título atualizado'
    assert data['concluida'] == True

def test_deletar_tarefa(client):
    """Testa deleção de tarefa"""
    response = client.delete('/tarefas/2')
    assert response.status_code == 200
    data = response.get_json()
    assert 'mensagem' in data

def test_deletar_tarefa_inexistente(client):
    """Testa deleção de tarefa que não existe"""
    response = client.delete('/tarefas/999')
    assert response.status_code == 404