# Exercício 3

Proxy opcional para build: BUILD_HTTP_PROXY/BUILD_HTTPS_PROXY no `.env`.
Veja [rede durante o build](../../README.md#rede-durante-o-build).

Execute em PowerShell, a partir da raiz do repositório:

```powershell
Set-Location docker/exercicio-3
Copy-Item .env.example .env # somente na primeira preparação; preserve seu .env existente
docker compose -f docker-compose.dev.yml config --quiet
docker compose -f docker-compose.dev.yml build
docker compose -f docker-compose.dev.yml up -d --wait
docker compose -f docker-compose.dev.yml logs -f api # Ctrl+C encerra a visualização dos logs
```

API: http://localhost:3002. Swagger: http://localhost:3002/docs.
As portas são publicadas apenas em 127.0.0.1.

O `.env.example` contém somente valores de demonstração. O `.env` local é ignorado pelo Git.
DB_HOST=db e DB_PORT=5432 são configurados diretamente no Compose; DB_USER,
DB_PASS e DB_NAME vêm do `.env`. Alterar as credenciais após inicializar o volume
não altera automaticamente os usuários existentes no PostgreSQL.

```powershell
'{"titulo":"Aprender Docker"}' | Set-Content -Encoding ascii tarefa.json
curl.exe -sS -X POST http://localhost:3002/tarefas -H "Content-Type: application/json" --data-binary '@tarefa.json'
Remove-Item tarefa.json
curl.exe -sS http://localhost:3002/tarefas
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml up -d --wait
curl.exe -sS http://localhost:3002/tarefas
```

POST retorna 201 com id e titulo. GET retorna uma lista. O título deve ser texto,
ter de 1 a 200 caracteres e não conter somente espaços; entradas inválidas retornam 422.
A criação da tabela usa `IF NOT EXISTS`, preservando os registros nos reinícios.
O INSERT parametrizado separa o texto recebido do comando SQL.
O último GET deve conter a tarefa anterior: `down` preserva o volume nomeado.

Na rede Compose, `db` é o nome DNS do PostgreSQL. `localhost` dentro da API
aponta para o próprio container, por isso não serve para acessar o banco.
A porta 5432 fica disponível na rede interna, sem publicação no host.
O healthcheck executa `pg_isready`; `depends_on: service_healthy` aguarda
essa prontidão inicial, mas não garante disponibilidade permanente.

## Dev e prod

O Dockerfile possui targets `dev` e `prod`, derivados da mesma base leve.
Dev monta `./api/app` em `/app/app`: o bind mount reflete alterações locais.
O Uvicorn usa `--reload` e reinicia ao salvar um arquivo Python.
Prod usa apenas o código copiado durante o build, sem bind mount e sem reload.
Ambos executam como usuário `app` (UID 10001).

```powershell
docker compose -f docker-compose.prod.yml config --quiet
docker compose -f docker-compose.prod.yml up -d --build --wait
curl.exe -sS http://localhost:3003/tarefas
docker compose -f docker-compose.prod.yml logs -f api
docker compose -f docker-compose.prod.yml down
```

Dev usa porta 3002/projeto `orion-ex3-dev`; prod usa porta 3003/projeto
`orion-ex3-prod`. Os prefixos dos projetos separam redes e volumes; uma tarefa
criada em dev não deve aparecer em prod. Os dois podem rodar simultaneamente.
Não use o mesmo `-p` nos dois comandos, pois isso substituiria esses nomes.
O volume do banco permanece em prod; a restrição do PDF é aplicada à montagem
do código-fonte, conforme orientação do pedido. “Prod” é a configuração de
produção do exercício, sem cobrir todos os requisitos de uma operação pública.
Para testar reload, altere temporariamente o título do FastAPI em `api/app/main.py`,
salve e consulte `/openapi.json`. Dev deve mudar e prod deve permanecer igual.
Depois restaure o arquivo.

## Encerramento

```powershell
docker compose -f docker-compose.dev.yml down
# DESTRUTIVO: remove os volumes e todos os dados deste projeto.
docker compose -f docker-compose.dev.yml down -v
```

A imagem oficial Python slim usa Debian reduzido e permite instalar wheels sem
compiladores adicionais. As dependências diretas são fixadas em requirements.txt.
Copiar requirements.txt antes do código permite reutilizar o cache de instalação.
`.dockerignore` exclui arquivos locais do contexto de build. O usuário sem root
reduz os privilégios da API. Não há importações dos outros exercícios.
