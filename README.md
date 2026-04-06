# 📝 API de Tarefas com Supabase

API simples para gerenciar tarefas usando Flask + Supabase.

## Pré-requisitos
- Python 3.12.3
- Conta no Supabase

### 1. Criar tabela no Supabase
```bash
CREATE TABLE tarefas (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    concluida BOOLEAN DEFAULT FALSE
);
```
## Endponits
- Método	➜ Endpoint ➜	O que faz
- GET ➜	/tarefas  ➜	Lista todas
- GET ➜	/tarefas/{id}  ➜	Busca uma
- POST ➜	/tarefas  ➜	Cria nova
- PUT ➜	/tarefas/{id} ➜	Atualiza
- DELETE ➜	/tarefas/{id} ➜	Deleta

## Comandos rápidos

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Crie um arquivo .env na raiz do projeto

```bash
SUPABASE_URL=sua_url_aqui
SUPABASE_KEY=sua_chave_aqui
```

### 3. Rodar API

```bash
python app.py
```

### 3. Rodar testes

```bash
pytest app_test.py -s -v
```
