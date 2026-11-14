import importlib
import sys
from pathlib import Path
from unittest.mock import patch
from fastapi.testclient import TestClient
import psycopg
import yaml

for ex in ('1', '2', '3', 'extra'):
    sys.path.insert(0, str(Path(f'docker/exercicio-{ex}/api').resolve()))
    m = importlib.import_module('app.main')
    client = TestClient(m.app)
    if ex == '1':
        response = client.get('/')
        assert response.status_code == 200 and response.content == b'Hello from Docker!'
        print('ex1: resposta exata OK (TestClient local)')
    else:
        for body in ({'titulo': ''}, {'titulo': '   '}, {'titulo': 'a'*201}, {'titulo': 12}, {}):
            assert client.post('/tarefas', json=body).status_code == 422
        with patch.object(m, 'connect', side_effect=psycopg.OperationalError('detalhe confidencial')):
            for method, path, kwargs in [('get','/tarefas',{}),('post','/tarefas',{'json':{'titulo':'ok'}})]:
                response = getattr(client,method)(path,**kwargs)
                assert response.status_code == 503 and 'confidencial' not in response.text
            if ex == 'extra':
                response = client.get('/health')
                assert response.status_code == 503 and response.json() == {'detail':'Banco indisponível'}
        print(f'ex{ex}: validação 422 e falhas 503 sem detalhes OK (falha simulada)')
    sys.path.pop(0)
    for key in list(sys.modules):
        if key == 'app' or key.startswith('app.'):
            del sys.modules[key]

dev = yaml.safe_load(Path('docker/exercicio-3/docker-compose.dev.yml').read_text())
prod = yaml.safe_load(Path('docker/exercicio-3/docker-compose.prod.yml').read_text())
assert dev['name'] != prod['name']
assert dev['services']['api']['ports'] != prod['services']['api']['ports']
assert 'volumes' not in prod['services']['api']
assert 'command' not in prod['services']['api']
assert prod['services']['db']['volumes']
assert '--reload' in dev['services']['api']['command']
print('ex3: isolamento de configuração, persistência prod, mount/reload dev OK')
