# Exercício extra

Execute em PowerShell, a partir da raiz do repositório:

```powershell
Set-Location docker/exercicio-extra
Copy-Item .env.example .env # somente na primeira preparação; preserve seu .env existente
docker compose config --quiet
docker compose build
docker compose up -d --wait
docker compose logs -f api # Ctrl+C encerra a visualização dos logs
```

API: http://localhost:3004. Swagger: http://localhost:3004/docs.
As portas são publicadas apenas em 127.0.0.1.

O `.env.example` contém somente valores de demonstração. O `.env` local é ignorado pelo Git.
DB_HOST=db e DB_PORT=5432 são configurados diretamente no Compose; DB_USER,
DB_PASS e DB_NAME vêm do `.env`. Alterar as credenciais após inicializar o volume
não altera automaticamente os usuários existentes no PostgreSQL.

```powershell
'{"titulo":"Aprender Docker"}' | Set-Content -Encoding ascii tarefa.json
curl.exe -sS -X POST http://localhost:3004/tarefas -H "Content-Type: application/json" --data-binary '@tarefa.json'
Remove-Item tarefa.json
curl.exe -sS http://localhost:3004/tarefas
docker compose down
docker compose up -d --wait
curl.exe -sS http://localhost:3004/tarefas
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

## Saúde e pgAdmin

```powershell
curl.exe -i http://localhost:3004/health
docker compose stop db
curl.exe -i http://localhost:3004/health
docker compose start db
```

Com banco disponível, `/health` executa `SELECT 1` e retorna 200 com
`{"status":"ok"}`. Sem banco, retorna 503 com mensagem genérica.
O timeout da conexão é 3 segundos e o das consultas é 5 segundos.

pgAdmin: http://localhost:8080. Entre usando PGADMIN_EMAIL e PGADMIN_PASSWORD
do `.env`. Em **Register > Server**, dê um nome e preencha **Connection**:
Host `db`, Port `5432`, Maintenance database igual a DB_NAME, Username igual
a DB_USER e Password igual a DB_PASS. Salve e abra o Query Tool:
`SELECT id, titulo FROM tarefas ORDER BY id;`.
O volume `pgadmin_data` preserva o cadastro. Os três serviços usam a rede `app`.
O código da API usa bind mount e reload neste ambiente de desenvolvimento.

## Encerramento

```powershell
docker compose down
# DESTRUTIVO: remove os volumes e todos os dados deste projeto.
docker compose down -v
```

A imagem oficial Python slim usa Debian reduzido e permite instalar wheels sem
compiladores adicionais. As dependências diretas são fixadas em requirements.txt.
Copiar requirements.txt antes do código permite reutilizar o cache de instalação.
`.dockerignore` exclui arquivos locais do contexto de build. O usuário sem root
reduz os privilégios da API. Não há importações dos outros exercícios.
