#Desenvolvido por Dionatan Rodrigues e Guilherme da Silva
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'online'
    assert 'mensagem' in data


def test_listar_tarefas(client):
    response = client.get('/tarefas')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)


def test_criar_tarefa_sucesso(client):
    response = client.post('/tarefas', json={'titulo': 'Teste pytest'})
    assert response.status_code == 201

    data = response.get_json()
    assert data['titulo'] == 'Teste pytest'
    assert data['concluida'] == False
    assert 'id' in data


def test_criar_tarefa_sem_titulo(client):
    response = client.post('/tarefas', json={'concluida': True})
    assert response.status_code == 400

    data = response.get_json()
    assert 'erro' in data


def test_buscar_tarefa_existente(client):
    # cria primeiro
    create = client.post('/tarefas', json={'titulo': 'Buscar tarefa'})
    tarefa = create.get_json()

    response = client.get(f"/tarefas/{tarefa['id']}")
    assert response.status_code == 200

    data = response.get_json()
    assert data['id'] == tarefa['id']


def test_buscar_tarefa_inexistente(client):
    response = client.get('/tarefas/999999')
    assert response.status_code == 404


def test_atualizar_tarefa(client):
    # cria primeiro
    create = client.post('/tarefas', json={'titulo': 'Atualizar tarefa'})
    tarefa = create.get_json()

    response = client.put(
        f"/tarefas/{tarefa['id']}",
        json={'titulo': 'Atualizado', 'concluida': True}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Atualizado'
    assert data['concluida'] == True


def test_deletar_tarefa(client):
    # cria primeiro
    create = client.post('/tarefas', json={'titulo': 'Deletar tarefa'})
    tarefa = create.get_json()

    response = client.delete(f"/tarefas/{tarefa['id']}")
    assert response.status_code == 200

    data = response.get_json()
    assert 'mensagem' in data


def test_deletar_tarefa_inexistente(client):
    response = client.delete('/tarefas/999999')
    assert response.status_code == 404